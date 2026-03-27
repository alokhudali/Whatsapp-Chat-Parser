import re

def parse_chat(file_path):
    pattern = re.compile(
        r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s(.+?)\s-\s([^:]+):\s?(.*)'
    )

    messages = []
    current_msg = None

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            match = pattern.match(line)

            if match:
                if current_msg:
                    messages.append(current_msg)

                date = match.group(1)
                time = match.group(2)
                sender = match.group(3).strip()
                message = match.group(4).strip()

                # ERROR sender → system message WITH prefix
                if sender.upper() == "ERROR":
                    full_message = f"ERROR: {message}"

                    current_msg = {
                        "timestamp": f"{date}, {time}",
                        "sender": "System",
                        "message": full_message,
                        "type": "system"
                    }
                    continue

                # Blank message
                if message == "":
                    message = "[Blank Message]"

                current_msg = {
                    "timestamp": f"{date}, {time}",
                    "sender": sender,
                    "message": message,
                    "type": "user"
                }

            else:
                # System message (no sender)
                if " - " in line:
                    if current_msg:
                        messages.append(current_msg)

                    timestamp, content = line.split(" - ", 1)

                    current_msg = {
                        "timestamp": timestamp.strip(),
                        "sender": "System",
                        "message": content.strip(),
                        "type": "system"
                    }

                else:
                    # Multiline
                    if current_msg:
                        current_msg["message"] += "\n" + line

    if current_msg:
        messages.append(current_msg)

    return messages