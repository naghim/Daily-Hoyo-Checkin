# Daily Hoyo Checkin

Aka a bot that checks in daily on certain anime waifu/husbando collector websites: namely the _"Official Grasscutter"_ and _"Ruby on Starry Rails"_.

# ltoken and ltuid Cookie Extraction Guide

This guide will walk you through the process of extracting the `ltoken` and `ltuid` values from the cookies on the daily check-in page using Google Chrome's developer tools.

## Prerequisites

Google Chrome browser installed on your computer.

## Steps

1. **Open the daily check-in page**: Open your Google Chrome browser. Navigate to the website and log in to your account if you haven't already.
2. **Open developer tools and find the cookies tab**: Once you are on the website and logged in, press F12 or right-click on any element on the page and select "Inspect" from the context menu. This will open the Chrome Developer Tools panel. In the Developer Tools panel, you will see several tabs. Click on the "Application" tab. This tab contains information about the website's cookies, among other things. In the left sidebar of the "Application" tab, expand the "Cookies" section. You will see various options like "Cookies," "Local Storage," and "Session Storage." Under the "Cookies" section, you should see a list of domains. Look for and click on the one related to the website.
3. **Find ltoken_v2 and ltuid_v2 cookies**: In the list of cookies for the game's domain, you should be able to find the `ltoken_v2` and `ltuid_v2` cookies.
4. **Copy the values**: To extract the ltoken and ltuid values, simply double-click on the respective cookie values, and it will allow you to copy them to your clipboard.

That's it! You have successfully extracted the ltoken and ltuid values from the website's cookies using Google Chrome's developer tools.

**Important Note:** Treat these values with care and do not share them with others, as they are sensitive authentication tokens and user identifiers.

# Running the script daily with GitHub Actions

## Steps

1. **Fork the project on GitHub**
2. **Create a new config file**: Use the ltoken and ltuid values found using Google Chrome. The config file should have the following format:

```json
{
  "healthcheck": "",
  "accounts": [
    {
      "name": "myaccount@gmail.com",
      "cookies": {
        "ltoken_v2": "AbCdEfGHIJKLmNOpqRSTuVwXyZ12345678901234",
        "ltuid_v2": "123456789"
      }
    }
  ]
}
```

3. **(Optional) Healthcheck**: In case you want to check if the workflow is successful, sign up on [Healthchecks](https://healthchecks.io/) and put the health check URL into the healthcheck field.
4. **Encode the config file into base64**: Visit [base64 encode](https://www.base64encode.org/) and encode the file in base64.
5. **Create the config file**: On GitHub, go to Settings > Security > Secrets and variables > Actions, then press "New repository secret", and save the base64 encoded config with the name `CHECKIN_CONFIG`.
6. **Activate GitHub Actions on the repository**: Select the "Allow all actions and reusable workflows" option from the list.
7. **Check if everything is okay**: Run the GitHub Actions workflow manually and check if it's successful. If it is successful, the script is set up to run every 6 hours. You can modify how often the script runs by editing the `.github/workflows/checkin.yaml` file. Use [crontab guru](https://crontab.guru) to create schedules.
