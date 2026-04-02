import json
import os
import csv
from typing import Dict, List

def save_messages(messages: Dict[str, List[int]], errors: List[str]):
    with open("messages.csv", "w", encoding='utf8') as f:
        f.write('channelid,messageid\n')
        for channel, ids in messages.items():
            if not ids:
                print(f'No messages found for channel: {channel} (skipping)')
                continue
            print(f'Saving messages from channel: {channel}')
            for id in ids:
                f.write(f'{channel},{id}\n')

    with open("dump_log.txt", "w", encoding='utf8') as f:
        total_messages = sum(len(ids) for ids in messages.values())
        total_channels = len(messages)
        skipped_channels = [ch for ch, ids in messages.items() if not ids]

        f.write(f"=== Dump Log ===\n")
        f.write(f"Total channels processed: {total_channels}\n")
        f.write(f"Total messages dumped: {total_messages}\n")
        f.write(f"Channels with no messages: {len(skipped_channels)}\n")
        f.write(f"Errors encountered: {len(errors)}\n\n")

        if skipped_channels:
            f.write("--- Channels with no messages ---\n")
            for ch in skipped_channels:
                f.write(f"  {ch}\n")
            f.write("\n")

        if errors:
            f.write("--- Errors ---\n")
            for error in errors:
                f.write(f"  {error}\n")
        else:
            f.write("--- No errors encountered ---\n")

def dump_dir(path: str, years: List[str], errors: List[str]) -> List[int]:
    messages = []
    if not os.path.isdir(path):
        errors.append(f"Path is not a directory: {path}")
        return messages

    if not os.path.exists(f'{path}/messages.json'):
        errors.append(f"Missing messages.json in: {path}")
        return messages

    print(f'Dumping messages from: {path}')
    try:
        with open(f'{path}/messages.json', 'r', encoding='utf8') as f:
            messages_obj = json.load(f)
            for message in messages_obj:
                try:
                    year = message["Timestamp"].split('-', 1)[0]
                    if year not in years:
                        continue
                    messages.append(message['ID'])
                except KeyError as e:
                    errors.append(f"Missing field {e} in message {message.get('ID', 'unknown')} in {path}")
                except Exception as e:
                    errors.append(f"Unexpected error on message {message.get('ID', 'unknown')} in {path}: {e}")
    except json.JSONDecodeError as e:
        errors.append(f"Failed to parse JSON in {path}: {e}")
    except Exception as e:
        errors.append(f"Unexpected error reading {path}: {e}")

    return messages

def dump_all(years: List[str], errors: List[str]) -> Dict[str, List[int]]:
    messages = {}
    try:
        channels = os.listdir('messages')
    except Exception as e:
        errors.append(f"Could not read messages directory: {e}")
        return messages

    for channel in channels:
        path = f'messages/{channel}'
        if not os.path.isdir(path):
            continue
        channel_id = channel.replace('c', '', 1)
        try:
            messages[channel_id] = dump_dir(path, years, errors)
        except Exception as e:
            errors.append(f"Unexpected error processing channel {channel_id}: {e}")

    return messages

def main():
    errors = []
    start = int(input("Enter start year (includes given year):\n> "))
    end = int(input("Enter end year (includes given year):\n> "))
    years = [str(y) for y in range(start, end + 1)]
    print(f'Filtering years: {", ".join(years)}')
    messages = dump_all(years, errors)
    save_messages(messages, errors)

if __name__ == "__main__":
    main()
    print("Dumped to messages.csv!")
    print("Log saved to dump_log.txt!")
    input("\nPress Enter to exit...")