import React, { useState } from 'react';
import './App.css';

function App() {
  const [dataSource, setDataSource] = useState('upload');
  const [file, setFile] = useState(null);
  const [dbConfig, setDbConfig] = useState({
    db_type: 'mysql',
    host: '',
    port: 3306,
    database: '',
    user: '',
    password: '',
    table: '',
  });
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const handleDataSourceChange = (event) => {
    setDataSource(event.target.value);
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleDbConfigChange = (event) => {
    const { name, value } = event.target;
    setDbConfig((prevConfig) => ({
      ...prevConfig,
      [name]: value,
    }));
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    console.log(data);
  };

  const handleConnect = async () => {
    const response = await fetch('/api/connect', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(dbConfig),
    });

    const data = await response.json();
    console.log(data);
  };

  const handleChat = async () => {
    const newChatHistory = [...chatHistory, { type: 'user', message: query }];
    setChatHistory(newChatHistory);

    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });

    const data = await response.json();
    setChatHistory([...newChatHistory, { type: 'bot', message: data.response }]);
    setQuery('');
  };

  return (
    <div className="App">
      <div className="sidebar">
        <h2>Data Source</h2>
        <div>
          <input
            type="radio"
            value="upload"
            checked={dataSource === 'upload'}
            onChange={handleDataSourceChange}
          />
          Upload CSV/Parquet
        </div>
        <div>
          <input
            type="radio"
            value="database"
            checked={dataSource === 'database'}
            onChange={handleDataSourceChange}
          />
          Connect to Database
        </div>

        {dataSource === 'upload' && (
          <div>
            <h3>Upload File</h3>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload</button>
          </div>
        )}

        {dataSource === 'database' && (
          <div>
            <h3>Database Connection</h3>
            <select name="db_type" value={dbConfig.db_type} onChange={handleDbConfigChange}>
              <option value="mysql">MySQL</option>
              <option value="postgres">PostgreSQL</option>
            </select>
            <input
              type="text"
              name="host"
              placeholder="Host"
              value={dbConfig.host}
              onChange={handleDbConfigChange}
            />
            <input
              type="number"
              name="port"
              placeholder="Port"
              value={dbConfig.db_type === 'mysql' ? 3306 : 5432}
              onChange={handleDbConfigChange}
            />
            <input
              type="text"
              name="database"
              placeholder="Database"
              value={dbConfig.database}
              onChange={handleDbConfigChange}
            />
            <input
              type="text"
              name="user"
              placeholder="User"
              value={dbConfig.user}
              onChange={handleDbConfigChange}
            />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={dbConfig.password}
              onChange={handleDbConfigChange}
            />
            <input
              type="text"
              name="table"
              placeholder="Table"
              value={dbConfig.table}
              onChange={handleDbConfigChange}
            />
            <button onClick={handleConnect}>Connect</button>
          </div>
        )}
      </div>
      <div className="main-content">
        <div className="chat-history">
          {chatHistory.map((chat, index) => (
            <div key={index} className={`chat-message ${chat.type}`}>
              {chat.message}
            </div>
          ))}
        </div>
        <div className="chat-input">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question about your data"
          />
          <button onClick={handleChat}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
