import requests
import random
import string
import uuid
from datetime import datetime


pas = "mahos99" #Change Your Password Here

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

        return requests.post(url, headers=headers, data=data).json()

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


def main():
    print("Choose Option:")
    print("[1] Send Reset via Email/Username")
    print("[2] Reset via ONE-CLICK Link")

    choice = input("Enter Option: ")

    if choice == "1":
        tg = input("Enter Email or Username: ")
        print(_sRst(tg))

    elif choice == "2":
        link = input("Enter Reset Link: ")
        print(_rLk(link))

    else:
        print("Invalid Option")


main()