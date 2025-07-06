from app.draft_assistant import get_drafts, get_draft_body, generate_reply, is_safe_draft

context = {
    "name": "Fatima",
    "subject": "Collaboration Opportunity",
    "topic": "ethical AI",
    "body": "I'd love to explore how our work might align and benefit the ummah."
}

email = generate_reply("reply_spiritual.j2", context)
print(email)

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
