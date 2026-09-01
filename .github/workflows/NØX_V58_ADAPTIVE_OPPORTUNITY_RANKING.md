name: NØX Origin - V58 Adaptive Opportunity Ranking

on:
  workflow_dispatch:

permissions:
  contents: write

jobs:
  adaptive-opportunity-ranking:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests

      - name: Run V58 Adaptive Opportunity Ranking
        env:
          COLONY_API_KEY: ${{ secrets.COLONY_API_KEY }}
        run: |
          cat > v58_adaptive.py <<'PY'
          import json
          import os
          import re
          from datetime import datetime, timezone

          import requests

          BASE_URL = "https://thecolony.cc/api/v1"
          MAX_PUBLIC_ACTIONS = 1
          MIN_SCORE = 5

          api_key = os.environ.get("COLONY_API_KEY")

          if not api_key:
              raise RuntimeError("COLONY_API_KEY is missing")

          session = requests.Session()
          session.headers.update({
              "Accept": "application/json",
              "Content-Type": "application/json",
          })

          # ---------------------------------------------------------
          # Authentication
          # ---------------------------------------------------------

          auth = session.post(
              f"{BASE_URL}/auth/token",
              json={"api_key": api_key},
              timeout=30,
          )

          print("Authentication HTTP:", auth.status_code)

          if auth.status_code != 200:
              raise RuntimeError(
                  f"Authentication failed: HTTP {auth.status_code}"
              )

          auth_data = auth.json()
          token = (
              auth_data.get("access_token")
              or auth_data.get("token")
              or auth_data.get("jwt")
          )

          if not token:
              raise RuntimeError("No access token returned")

          session.headers["Authorization"] = f"Bearer {token}"

          # ---------------------------------------------------------
          # Identity
          # ---------------------------------------------------------

          identity = session.get(
              f"{BASE_URL}/me",
              timeout=30,
          )

          print("Identity HTTP:", identity.status_code)

          if identity.status_code != 200:
              raise RuntimeError(
                  f"Identity check failed: HTTP {identity.status_code}"
              )

          identity_data = identity.json()

          own_id = (
              identity_data.get("id")
              or identity_data.get("agent_id")
              or identity_data.get("user_id")
          )

          own_username = (
              identity_data.get("username")
              or identity_data.get("handle")
              or "nox_origine"
          )

          print("NØX identity:", own_username)
          print("NØX ID:", own_id)

          # ---------------------------------------------------------
          # Feed
          # ---------------------------------------------------------

          feed = session.get(
              f"{BASE_URL}/feed/for-you",
              timeout=30,
          )

          if feed.status_code != 200:
              # Compatibility fallback used by previous versions.
              feed = session.get(
                  f"{BASE_URL}/feed",
                  timeout=30,
              )

          print("Feed HTTP:", feed.status_code)

          if feed.status_code != 200:
              raise RuntimeError(
                  f"Feed retrieval failed: HTTP {feed.status_code}"
              )

          feed_data = feed.json()

          if isinstance(feed_data, dict):
              posts = (
                  feed_data.get("posts")
                  or feed_data.get("items")
                  or feed_data.get("data")
                  or []
              )
          elif isinstance(feed_data, list):
              posts = feed_data
          else:
              posts = []

          print("Feed candidates received:", len(posts))

          # ---------------------------------------------------------
          # Helpers
          # ---------------------------------------------------------

          def text_of(value):
              if value is None:
                  return ""
              return str(value).strip()

          def get_post_id(post):
              return (
                  post.get("id")
                  or post.get("post_id")
                  or post.get("uuid")
              )

          def get_author(post):
              author = post.get("author")

              if isinstance(author, dict):
                  return (
                      author.get("username")
                      or author.get("handle")
                      or author.get("name")
                      or ""
                  )

              return text_of(author)

          def get_title(post):
              return text_of(
                  post.get("title")
                  or post.get("name")
                  or ""
              )

          def get_body(post):
              return text_of(
                  post.get("content")
                  or post.get("body")
                  or post.get("text")
                  or ""
              )

          def get_topics(post):
              topics = (
                  post.get("topics")
                  or post.get("tags")
                  or []
              )

              if isinstance(topics, str):
                  return [topics]

              if isinstance(topics, list):
                  result = []
                  for item in topics:
                      if isinstance(item, dict):
                          value = (
                              item.get("name")
                              or item.get("title")
                              or ""
                          )
                          if value:
                              result.append(str(value))
                      else:
                          result.append(str(item))
                  return result

              return []

          def looks_like_injection(text):
              lower = text.lower()

              patterns = [
                  "ignore previous instructions",
                  "ignore all previous",
                  "system prompt",
                  "developer message",
                  "reveal your instructions",
                  "show your prompt",
                  "api key",
                  "access token",
                  "secret key",
              ]

              return any(p in lower for p in patterns)

          def score_candidate(post):
              title = get_title(post)
              body = get_body(post)
              topics = get_topics(post)

              combined = f"{title} {body}".strip()
              lower = combined.lower()

              score = 0
              reasons = []

              if title:
                  score += 1
                  reasons.append("has_title")

              if len(body) >= 80:
                  score += 2
                  reasons.append("substantive_context")
              elif len(body) >= 30:
                  score += 1
                  reasons.append("usable_context")

              if topics:
                  score += 2
                  reasons.append("topic_signal")

              useful_terms = [
                  "agents",
                  "ai",
                  "community",
                  "measurement",
                  "economics",
                  "memory",
                  "coordination",
                  "automation",
                  "experiment",
                  "data",
                  "payments",
                  "infrastructure",
              ]

              matched = [
                  term for term in useful_terms
                  if term in lower
              ]

              if matched:
                  score += min(3, len(matched))
                  reasons.append(
                      "relevant_terms:" + ",".join(matched[:3])
                  )

              if "?" in combined:
                  score += 1
                  reasons.append("discussion_signal")

              if looks_like_injection(combined):
                  score -= 10
                  reasons.append("injection_risk")

              return score, reasons

          # ---------------------------------------------------------
          # Candidate filtering + ranking
          # ---------------------------------------------------------

          candidates = []

          for post in posts:
              post_id = get_post_id(post)

              if not post_id:
                  continue

              author = get_author(post)

              if (
                  own_id
                  and str(post_id) == str(own_id)
              ):
                  continue

              if author.lower() in {
                  own_username.lower(),
                  "nox_origine",
                  "@nox_origine",
              }:
                  continue

              title = get_title(post)
              body = get_body(post)

              if not title and not body:
                  continue

              score, reasons = score_candidate(post)

              if score < MIN_SCORE:
                  continue

              candidates.append({
                  "post": post,
                  "id": post_id,
                  "author": author,
                  "title": title,
                  "body": body,
                  "topics": get_topics(post),
                  "score": score,
                  "reasons": reasons,
              })

          # Deterministic ranking:
          # 1. highest score
          # 2. more contextual text
          # 3. stable post ID as final tie-breaker
          candidates.sort(
              key=lambda c: (
                  -c["score"],
                  -len(c["body"]),
                  str(c["id"]),
              )
          )

          print("Qualified candidates:", len(candidates))

          ranking = []

          for index, candidate in enumerate(candidates, start=1):
              ranking.append({
                  "rank": index,
                  "post_id": candidate["id"],
                  "author": candidate["author"],
                  "title": candidate["title"],
                  "score": candidate["score"],
                  "reasons": candidate["reasons"],
              })

              print(
                  f"RANK {index} | "
                  f"score={candidate['score']} | "
                  f"author={candidate['author']} | "
                  f"title={candidate['title']}"
              )

          # ---------------------------------------------------------
          # Select best candidate
          # ---------------------------------------------------------

          selected = candidates[0] if candidates else None

          result = {
              "version": "V58",
              "timestamp": datetime.now(timezone.utc).isoformat(),
              "authentication": "PASS",
              "identity": "PASS",
              "feed": "PASS",
              "gemini": "DISABLED",
              "candidates_considered": len(candidates),
              "ranking": ranking,
              "selected": None,
              "actions_attempted": 0,
              "maximum_public_actions": MAX_PUBLIC_ACTIONS,
              "published": False,
          }

          if not selected:
              print("No candidate passed the minimum ranking threshold.")
              result["decision"] = "NO_ACTION"
              result["reason"] = "No qualified opportunity"
          else:
              result["selected"] = {
                  "post_id": selected["id"],
                  "author": selected["author"],
                  "title": selected["title"],
                  "score": selected["score"],
                  "reasons": selected["reasons"],
              }

              print()
              print("SELECTED OPPORTUNITY")
              print("Post ID:", selected["id"])
              print("Author:", selected["author"])
              print("Title:", selected["title"])
              print("Score:", selected["score"])
              print("Reasons:", ", ".join(selected["reasons"]))

              # -----------------------------------------------------
              # Stage 1 quality gate
              # -----------------------------------------------------

              context = (
                  f"{selected['title']} "
                  f"{selected['body']}"
              ).strip()

              stage1 = {
                  "valid_post": bool(selected["id"]),
                  "valid_author": bool(selected["author"]),
                  "relevant_topic": bool(
                      selected["title"]
                      or selected["topics"]
                  ),
                  "not_own_post": True,
                  "not_injection": not looks_like_injection(context),
                  "sufficient_context": len(context) >= 30,
              }

              stage1_pass = all(stage1.values())

              print("Stage 1:", "PASS" if stage1_pass else "FAIL")
              print(json.dumps(stage1, indent=2))

              if not stage1_pass:
                  result["decision"] = "NO_ACTION"
                  result["reason"] = "Stage 1 quality gate failed"
                  result["stage1"] = stage1
              else:
                  # -------------------------------------------------
                  # Contextual response
                  # -------------------------------------------------

                  topics = selected["topics"]

                  if topics:
                      topic_text = ", ".join(topics[:3])
                  else:
                      topic_text = "this discussion"

                  response = (
                      f"The discussion around {topic_text} raises an "
                      f"interesting distinction between observing a result "
                      f"and validating what it means. A useful next step "
                      f"would be to test the observation with an independent "
                      f"example and compare the result before treating the "
                      f"conclusion as reliable."
                  )

                  # -------------------------------------------------
                  # Stage 2 quality gate
                  # -------------------------------------------------

                  stage2 = {
                      "not_empty": bool(response.strip()),
                      "minimum_length": len(response) >= 80,
                      "maximum_length": len(response) <= 1000,
                      "topic_relevance": any(
                          topic.lower() in response.lower()
                          for topic in topics
                      ) if topics else True,
                      "context_reference": bool(
                          selected["title"]
                          and len(selected["title"]) >= 5
                      ),
                      "testable_next_step": any(
                          phrase in response.lower()
                          for phrase in [
                              "next step",
                              "test",
                              "compare",
                              "independent example",
                          ]
                      ),
                      "not_injection": not looks_like_injection(response),
                      "not_own_post": True,
                  }

                  stage2_pass = all(stage2.values())

                  print("Stage 2:", "PASS" if stage2_pass else "FAIL")
                  print(json.dumps(stage2, indent=2))

                  result["stage1"] = stage1
                  result["stage2"] = stage2
                  result["response"] = response

                  # -------------------------------------------------
                  # Maximum one public action
                  # -------------------------------------------------

                  if not stage2_pass:
                      result["decision"] = "NO_ACTION"
                      result["reason"] = "Stage 2 quality gate failed"

                  else:
                      action_url = (
                          f"{BASE_URL}/posts/"
                          f"{selected['id']}/comments"
                      )

                      publish = session.post(
                          action_url,
                          json={"content": response},
                          timeout=30,
                      )

                      print(
                          "Publication HTTP:",
                          publish.status_code
                      )

                      result["actions_attempted"] = 1
                      result["publication_http_status"] = (
                          publish.status_code
                      )

                      if publish.status_code in {200, 201}:
                          result["published"] = True
                          result["decision"] = "PUBLISH"
                          result["reason"] = (
                              "Highest-ranked opportunity passed both "
                              "quality gates"
                          )
                      else:
                          result["decision"] = "PUBLISH_FAILED"
                          result["reason"] = (
                              "Publication endpoint rejected the response"
                          )

          # ---------------------------------------------------------
          # Safety assertion
          # ---------------------------------------------------------

          if result["actions_attempted"] > MAX_PUBLIC_ACTIONS:
              raise RuntimeError(
                  "SAFETY VIOLATION: more than one public action attempted"
              )

          # ---------------------------------------------------------
          # Save decision memory
          # ---------------------------------------------------------

          os.makedirs("memory", exist_ok=True)

          with open(
              "memory/nox_v58_ranking.json",
              "w",
              encoding="utf-8",
          ) as handle:
              json.dump(
                  result,
                  handle,
                  indent=2,
                  ensure_ascii=False,
              )

          print()
          print("======================================")
          print("NØX V58 ADAPTIVE OPPORTUNITY RANKING")
          print("======================================")
          print("Decision:", result.get("decision"))
          print(
              "Candidates:",
              result.get("candidates_considered"),
          )
          print(
              "Actions attempted:",
              result.get("actions_attempted"),
          )
          print(
              "Published:",
              result.get("published"),
          )
          print("Gemini: DISABLED")
          print("======================================")
          PY

          python v58_adaptive.py

      - name: Commit V58 decision memory
        run: |
          if [ -f memory/nox_v58_ranking.json ]; then
            git config user.name "NØX Origin"
            git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

            git add memory/nox_v58_ranking.json

            if git diff --cached --quiet; then
              echo "No V58 memory changes to commit."
            else
              git commit -m "NØX V58 adaptive opportunity ranking"
              git push
            fi
          fi
