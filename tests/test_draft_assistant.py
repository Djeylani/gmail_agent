from app.draft_assistant import get_drafts, get_draft_body, generate_reply, is_safe_draft

drafts = get_drafts()

for draft in drafts:
    draft_id = draft['id']
    body = get_draft_body(draft_id)
    if not body:
        print("⚠️ No body found in draft.")
        continue

    if not is_safe_draft(body):
        print("🔒 Skipping sensitive draft.")
        continue

    print(f"\n✉️ Draft:\n{body}")
    reply = generate_reply(body)
    print(f"\n🤖 Suggested Reply:\n{reply}")
