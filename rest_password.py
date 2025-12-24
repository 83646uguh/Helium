import requests
import random
import string
import uuid
from datetime import datetime
import time

pas = "mahos99"  # Change Your Password Here

def _gDv():
    aid = f"android-{''.join(random.choices(string.hexdigits.lower(), k=16))}"

    ua = (
        f"Instagram 394.0.0.46.81 Android "
        f"({random.choice(['29/10', '30/11', '31/12'])}; "
        f"{random.choice(['320dpi', '480dpi'])}; "
        f"{random.choice(['720x1280', '1080x1920'])}; "
        f"{random.choice(['samsung', 'xiaomi', 'google'])}; "
        f"{random.choice(['SM-G975F', 'Mi-9T', 'Pixel-4'])}; "
        f"en_US; {random.randint(100000000, 999999999)})"
    )

    wf = str(uuid.uuid4())
    ts = int(datetime.now().timestamp())
    pw = f"#PWD_INSTAGRAM:0:{ts}:{pas}"

    return aid, ua, wf, pw


def _hX(md="", ua=""):
    return {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Bloks-Version-Id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
        "X-Mid": md,
        "User-Agent": ua,
    }


def _sRst(tag):
    try:
        url = "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/"
        headers = {
            "user-agent": "Mozilla/5.0",
            "content-type": "application/x-www-form-urlencoded",
            "x-csrftoken": "umwHlWf6r3AGDowkZQb47m",
            "x-instagram-ajax": "1018880011",
            "x-requested-with": "XMLHttpRequest",
        }
        data = {"email_or_username": tag, "flow": "fxcal"}

        response = requests.post(url, headers=headers, data=data)
        return response.json()

    except Exception as e:
        return {"ok": False, "error": str(e)}


def make_headers(mid="", user_agent=""):
    return {
        "User-Agent": user_agent,
        "X-Mid": mid,
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Bloks-Version-Id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
    }


def _rLk(reset_link):
    try:
        ANDROID_ID, USER_AGENT, WATERFALL_ID, PASSWORD = _gDv()

        uidb36 = reset_link.split("uidb36=")[1].split("&token=")[0]
        token = reset_link.split("&token=")[1].split(":")[0]

        url = "https://i.instagram.com/api/v1/accounts/password_reset/"
        data = {
            "source": "one_click_login_email",
            "uidb36": uidb36,
            "device_id": ANDROID_ID,
            "token": token,
            "waterfall_id": WATERFALL_ID
        }

        r = requests.post(url, headers=make_headers(user_agent=USER_AGENT), data=data)

        if "user_id" not in r.text:
            return {"success": False, "error": r.text}

        mid = r.headers.get("Ig-Set-X-Mid")
        resp = r.json()
        print(resp)

        user_id = resp.get("user_id")
        cni = resp.get("cni")
        nonce_code = resp.get("nonce_code")
        challenge_context = resp.get("challenge_context")

        url2 = "https://i.instagram.com/api/v1/bloks/apps/com.instagram.challenge.navigation.take_challenge/"
        data2 = {
            "user_id": str(user_id),
            "cni": str(cni),
            "nonce_code": str(nonce_code),
            "bk_client_context": (
                '{"bloks_version":"e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",'
                '"styles_id":"instagram"}'
            ),
            "challenge_context": str(challenge_context),
            "bloks_versioning_id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
            "get_challenge": "true"
        }

        r2 = requests.post(url2, headers=make_headers(mid, USER_AGENT), data=data2).text
        
        if str(cni) not in r2:
            return {"success": False, "error": "Challenge failed"}

        challenge_final = r2.replace("\\", "").split(f"(bk.action.i64.Const, {cni}), \"")[1].split(
            "\", (bk.action.bool.Const, false)))"
        )[0]

        data3 = {
            "is_caa": "False",
            "cni": str(cni),
            "challenge_context": challenge_final,
            "bloks_versioning_id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
            "enc_new_password1": PASSWORD,
            "enc_new_password2": PASSWORD
        }

        ah = requests.post(url2, headers=make_headers(mid, USER_AGENT), data=data3)
        
        new_password = PASSWORD.split(":")[-1]
        return {"success": True, "password": new_password}

    except Exception as e:
        return {"success": False, "error": str(e)}


def send_multiple_resets(tag, count=50):
    """Send multiple reset requests"""
    results = []
    
    print(f"\nStarting to send {count} reset requests for: {tag}")
    print("-" * 50)
    
    for i in range(1, count + 1):
        try:
            print(f"\nRequest #{i}:")
            result = _sRst(tag)
            
            # Display response
            if "ok" in result:
                print(f"Response: {result}")
            else:
                print(f"Response: Error - {result.get('error', 'Unknown error')}")
            
            results.append(result)
            
            # Add small delay to avoid rate limiting (adjust as needed)
            if i < count:
                time.sleep(0.5)
                
        except Exception as e:
            print(f"Request #{i} failed: {str(e)}")
            results.append({"ok": False, "error": str(e)})
    
    print("-" * 50)
    print(f"\nCompleted {len(results)} requests")
    
    # Summary
    successful = sum(1 for r in results if r.get("ok") == True)
    failed = len(results) - successful
    
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    return results


def main():
    print("Choose Option:")
    print("[1] Send Reset via Email/Username (50 times)")
    print("[2] Reset via ONE-CLICK Link")

    choice = input("Enter Option: ")

    if choice == "1":
        tg = input("Enter Email or Username: ")
        confirm = input(f"Are you sure you want to send 50 reset requests to '{tg}'? (y/n): ")
        
        if confirm.lower() == 'y':
            send_multiple_resets(tg, 50)
        else:
            print("Operation cancelled.")

    elif choice == "2":
        link = input("Enter Reset Link: ")
        print(_rLk(link))

    else:
        print("Invalid Option")


if __name__ == "__main__":
    main()
