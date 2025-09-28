<h1 align="center" style="color:#1a73e8;">Next-Gen RAG News Verification Engine 📰</h1>

<div align="center">
  <img src="https://img.icons8.com/fluency/120/news.png" alt="News Icon"/>
</div>

---

<h2 style="color:#34a853;">Overview</h2>

<p>
The <strong>Next-Gen RAG News Verification Engine</strong> is a web-based application that leverages <strong>AI and RAG (Retrieval-Augmented Generation)</strong> to verify news from multiple online sources like Google, Bing, Reddit, X (Twitter), and more. It provides:
</p>

<ul>
  <li>🧠 AI-generated answers with <strong>supporting sources</strong></li>
  <li>📄 Display of <strong>full articles</strong> for context</li>
  <li>🎨 Elegant <strong>glassmorphic search engine UI</strong></li>
  <li>🔗 Easy integration for additional sources</li>
</ul>

---

<h2 style="color:#fbbc05;">Features</h2>

<ul>
  <li>🔍 Multi-source internet search for news verification</li>
  <li>🤖 ChatGPT-powered AI reasoning and answer generation</li>
  <li>📚 Full article preview from sources</li>
  <li>🖼️ Modern <strong>glassmorphic UI</strong> built with Bootstrap</li>
  <li>🌐 Expandable to custom sources and datasets</li>
</ul>

---

<h2 style="color:#ea4335;">Tech Stack</h2>

<table>
<tr>
<th>Category</th><th>Technology</th>
</tr>
<tr>
<td>Backend</td><td>Python, Flask</td>
</tr>
<tr>
<td>AI & Tools</td><td>OpenAI GPT, LangGraph, LangChain</td>
</tr>
<tr>
<td>Frontend</td><td>HTML5, CSS3, Bootstrap 5, Glassmorphism</td>
</tr>
<tr>
<td>API Services</td><td>BrightData (web scraping & search results)</td>
</tr>
<tr>
<td>Environment</td><td>Python-dotenv</td>
</tr>
</table>

---

<h2 style="color:#1a73e8;">Installation</h2>

<pre>
git clone https://github.com/Bibek257/Next-Gen-Search-Engine.git
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
</pre>

<p>Create a <strong>.env</strong> file in the root directory:</p>

<pre>
OPENAI_API_KEY=your_openai_api_key
BRIGHTDATA_API_KEY=your_brightdata_api_key
BRIGHTDATA_SERP_ZONE=your_serp_zone
BRIGHTDATA_GPT_DATASET_ID=your_gpt_dataset_id
BRIGHTDATA_PREPLEXITY_DATASET_ID=your_preplexity_dataset_id
</pre>

---

<h2 style="color:#34a853;">Usage</h2>

<pre>
python app.py
</pre>

<p>Then open your browser:</p>

<pre>
http://127.0.0.1:5000/
</pre>

<p>Enter your news query in the search box. You will get:</p>

<ul>
<li>AI-generated answer</li>
<li>Sources of the information</li>
<li>Full article content</li>
</ul>

---

<h2 style="color:#fbbc05;">How It Works</h2>

<ol>
<li><strong>User Query:</strong> User enters a news topic or headline.</li>
<li><strong>RAG Processing:</strong> Searches multiple sources via BrightData API.</li>
<li><strong>AI Reasoning:</strong> ChatGPT processes collected data and generates a verified answer.</li>
<li><strong>Output Display:</strong> Answer, sources, and full articles displayed in glassmorphic UI.</li>
</ol>

<h2 style="color:#1a73e8;">Contributing</h2>

<p>Contributions are welcome! You can:</p>

<ul>
<li>Add more search sources</li>
<li>Improve AI prompts for better accuracy</li>
<li>Enhance the front-end UI</li>
</ul>

---

<h2 style="color:#34a853;">License</h2>

<p>This project is <strong>MIT Licensed</strong>. See <code>LICENSE</code> for details.</p>

---

<h2 style="color:#fbbc05;">Contact</h2>

<p>
<strong>BIBEK GHIMIRE</strong><br>
Email: <a href="mailto:gbibek257@gmail.com">gbibek257@gmail.com</a><br>
</p>
