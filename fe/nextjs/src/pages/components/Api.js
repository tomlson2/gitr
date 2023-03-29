import React, { useState } from 'react';
import styles from './Api.module.css';
import { generateApi } from '../api/api';

const Api = () => {
  const [apiResult, setApiResult] = useState('');
  const [repoName, setRepoName] = useState('');

  const handleGenerateApi = async () => {
    const result = await generateApi(repoName);
    setApiResult(result);
  };

  return (
    <div className={styles.container}>
      <h1>Generate API</h1>
      <div className={styles.inputContainer}>
        <input
          type="text"
          placeholder="Repository Name"
          value={repoName}
          onChange={(e) => setRepoName(e.target.value)}
        />
        <button onClick={handleGenerateApi}>Generate API</button>
      </div>
        <div className={styles.apiResult}>
          <h2>API Result:</h2>
          <pre>{apiResult}</pre>
        </div>
    </div>
  );
};

export default Api;
