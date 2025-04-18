# 📚 TDS Assignment Solver

This project helps you automatically solve graded assignment questions for the **Tools in Data Science** course at  **IIT Madras' Online Degree in Data Science** .

---

## 📘 Background

This project is built to assist students of the **IIT Madras Online BSc Degree in Data Science**, specifically in the **Tools in Data Science** course.

This solution relies on **direct function-calling** logic to accurately answer questions from **graded assignments**.

The goal is to create an **API** that accepts a question (and optionally, a file), then processes it using pre-defined logic and functions, and returns the final answer in JSON format.

---

## 🚀 API Overview

### 📌 Endpoint

**POST :** `https://your-app.vercel.app/api/`

The above endpoint is an example. The actual endpoint will depend on the deployment portal you choose (e.g., Vercel, Azure). Replace this URL with your actual deployed URL once the application is live.

### 🔧 Request Format

Use `multipart/form-data` format with:

* `question`: (string) the task or question
* `file`: (optional) file attachments

#### ✅ Example Request (using `curl`):

```bash
curl -X POST "https://your-app.vercel.app/api/" \
  -H "Content-Type: multipart/form-data" \
  -F "question=Download and unzip file abcd.zip which has a single extract.csv file inside. What is the value in the 'answer' column of the CSV file?" \
  -F "file=@abcd.zip"
```

### 📥 Response Format :

JSON Object or Stringified JSON Object:

```json
{
  "answer": "1234567890"
}
```

---

## ☁️ Deploy Your Application

You can deploy your application using  **Vercel** ,  **Azure** , or any cloud provider.

### 🔷 Azure Deployment Steps

#### 1. Create Resources

* Login to [Azure Portal](https://portal.azure.com/)
* Create a **Resource Group**
* Create an **App Service** (Web App)

#### 2. Enable FTP/FTPS Authentication

* Go to your Web App
* Navigate to **Settings > Configuration**
* Under  **General Settings** , set **FTP State** to `FTPS Only`
* Click **Save**

#### 3. Reset FTPS Credentials (Optional)

* Go to **Deployment Center > FTPS Credentials**
* Reset credentials if needed

#### 4. Set Startup Script

* In the **Configuration** section, under  **General Settings** , set **Startup Command** to:

  ```
  ./startup.sh
  ```

#### 5. Set Environment Variables

In the **Configuration > Application settings**, add the following environment variables:

| Name              | Value                |
| ----------------- | -------------------- |
| `AIPROXY_TOKEN` | Your API Proxy Token |
| `username`      | Your GitHub Username |
| `github_token`  | Your GitHub Token    |

#### 6. Use Local Git for Deployment

* In  **Deployment Center** , choose **Local Git** as the deployment method

##### 📌 Steps to Deploy:

1. **Copy Git Clone URL & Credentials**
   * From FTPS tab in Deployment Center, copy the Git URL, username, and password
2. **Initialize Git in Your Project**

```bash
git init
git add .
git commit -m "Initial commit"
```

3. **Add Azure Remote and Push Code**

```bash
git remote add azure <Git Clone URL>
git push azure master
```

> 🔒 You may be prompted to enter the username and password you copied from the Azure Deployment Center.

---

## 🔍 Evaluation Criteria

* Can your API answer a variety of assignment questions?
* Can it handle file processing?
* Is the answer accurate and formatted properly?

---

## 🧠 Technologies Used

* Python
* FastAPI / Flask (for API)
* OpenAI / Hugging Face APIs (for LLM)
* Vercel or Azure (for deployment)
