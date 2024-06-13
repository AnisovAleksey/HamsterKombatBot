# Guide on extracting authorization information on Android

## Steps

### 1. Enable Developer Mode and USB Debugging

1. Go to **Settings** on your Android device.
2. Find **About phone** or **About tablet**.
3. Tap on **Build number** several times (typically 7 times) until you see "You are now a developer".
4. Go back to **Settings** and find the new **Developer options** section.
5. Enable **Developer mode** and **USB debugging**.

### 2. Enable Debugging Mode in Telegram

1. Open Telegram on your device.
2. Go to **Settings**.
3. Scroll down to the bottom and long press two times on **Telegram Version**.
4. In the menu that appears, select **Enable Web View Inspecting**.

### 3. Connect Device to PC

1. Connect your Android device to your computer using a USB cable.
2. You will see a prompt on your device to allow USB debugging - confirm it.

### 4. Open DevTools in Chrome

1. Open Google Chrome on your PC.
2. Enter `chrome://inspect/#devices` in the address bar and press Enter.

### 5. Debug Web View

1. On your device, open Telegram and navigate to the HamsterKombat bot.
2. In Chrome, find your device in the list and choose any of the available Hamster Kombat processes. ![alt text](image.png)
3. Click on **inspect**.

### 6. Using DevTools

1. DevTools will open in a new window. Go to the **Network** tab. ![newtork-tab](https://github.com/Sanlovty/HamsterKombatBot_prs/assets/68380831/b2cb512c-b10c-4286-84d5-60deb58454e6)

2. Go to the **earn** tab to generate an HTTP request. ![earn-tab](https://github.com/Sanlovty/HamsterKombatBot_prs/assets/68380831/268dad87-6919-44fe-9eab-de1d98a40d9d)

3. Enter `list-task` in the search bar and select the `Fetch/XHR` filter. ![filters](https://github.com/Sanlovty/HamsterKombatBot_prs/assets/68380831/d03fc2e2-70aa-47ba-97c8-6b5c8a2d8391)

4. Click on the request to open the interaction menu with the HTTP request. ![open-request](https://github.com/Sanlovty/HamsterKombatBot_prs/assets/68380831/b69a8cf6-8f3a-4afa-84fd-d3a644bf80e5)

5. In the opened window, under **Headers**, navigate to **Request Headers**. ![open-request-data](https://github.com/Sanlovty/HamsterKombatBot_prs/assets/68380831/77265bea-0eb5-4a19-b41a-4af114d17dba)

6. Copy the token in the **Authorization:** attribute and remove `Bearer`, leaving only the token.
   For example: `Bearer 9aFJ6C29b81cLmR04DKq7fXzQi52tHOG8e7R9vUj6iPcYwTxN0uMbA3SdV5Ks2WjMnLv8qZoJ3F1rY46tQm9` should become `9aFJ6C29b81cLmR04DKq7fXzQi52tHOG8e7R9vUj6iPcYwTxN0uMbA3SdV5Ks2WjMnLv8qZoJ3F1rY46tQm9`.
   This is your token. ![fields](https://github.com/Sanlovty/HamsterKombatBot_prs/assets/68380831/410a4a77-bfcd-46fb-8151-6dcb74965e41)

7. All the other fields, highlighted in yellow [`Accept-Encoding`,`Accept-Language`,`Sec-Ch-Ua`,`Sec-Ch-Ua-Mobile`,`Sec-Ch-Ua-Platform`] can be used to generate a custom **headers** in [headers.py](https://github.com/AnisovAleksey/HamsterKombatBot/blob/b66014360c5664c27936378c7b611feb5b6c46dd/bot/core/headers.py).
