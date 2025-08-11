import os
from dotenv import load_dotenv

from app.agent import build_agent


def main():
    load_dotenv()
    thread_id = os.getenv("DEMO_THREAD_ID", "u1:chat-001")
    user_id = os.getenv("DEMO_USER_ID", "u1")

    agent = build_agent()

    print("--- Streaming agent updates ---")
    for update in agent.stream(
        {"messages": "Remember: my name is Bob"},
        context={"thread_id": thread_id, "user_id": user_id},
        stream_mode="updates",
    ):
        for k, v in update.items():
            print(f"[{k}] {getattr(v, 'type', type(v))}")

    final = agent.invoke(
        {"messages": "What's my name?"},
        context={"thread_id": thread_id, "user_id": user_id},
    )
    print("--- Final message ---")
    print(final["messages"][-1].content)


if __name__ == "__main__":
    main()
