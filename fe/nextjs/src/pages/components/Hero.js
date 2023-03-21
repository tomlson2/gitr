import React, { useState } from 'react';
import styles from './Hero.module.css';
import ReactMarkdown from 'react-markdown';
import {Prism as SyntaxHighlighter} from 'react-syntax-highlighter';
import useTypewriter from '../hooks/useTypewriter';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faExternalLinkAlt } from '@fortawesome/free-solid-svg-icons';
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';
import { faPencilAlt } from '@fortawesome/free-solid-svg-icons';
import { generateReadme, createPullRequest, updateReadme } from '../api/api';

const Hero = () => {
  const [readme, setReadme] = useState('');
  const [hasReadme, setHasReadme] = useState(false);
  const [repo, setRepo] = useState('');
  const [generating, startedGenerating] = useState(false);
  const [link, setLink] = useState('');
  const [update, setUpdate] = useState('');
  const [markdownKey, setMarkdownKey] = useState(0);

  const typedReadme = useTypewriter(readme, 5);

  const handleGenerateReadme = async () => {
    startedGenerating(true);
    const generatedReadme = await generateReadme(repo);
    startedGenerating(false);
    setReadme(generatedReadme);
    setHasReadme(true);
  };

  const handlePullRequest = async () => {
    const pullRequestLink = await createPullRequest(repo, readme);
    setLink(pullRequestLink);
  };

  const handleChanges = async () => {
    startedGenerating(true);
    setHasReadme(false);
    const updatedReadme = await updateReadme(readme, update);
    startedGenerating(false);
    setReadme(updatedReadme);
    setHasReadme(true);
    setMarkdownKey(markdownKey + 1);
  };

  function getCookie(name) {
    if (typeof window !== 'undefined') {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    }
  }
  
  const userLogin = getCookie('userLogin');
  
  return (
    <div className={styles.hero}>
      <div className={styles.content}>
        <h1>WRITEME.md</h1>
        <p>Automatically generate READMEs for your GitHub repositories</p>
        {!userLogin && <p>You are not logged in.</p>}
        {userLogin && <div className={styles.inputcontainer}>
          <input type="text" placeholder="Repository Owner"  value={userLogin} readOnly />
          <input type="text" placeholder="Repository Name"  value={repo} onChange={(e) => setRepo(e.target.value)}/>
          <button onClick={handleGenerateReadme}>
            Generate README <span className={styles.iconWrapper}><FontAwesomeIcon icon={faPencilAlt} /></span>
            </button>
        </div>}
        {generating && <div className={styles.readmecontainer}>
          <span className={styles.cursor}></span>
        </div>}
        {hasReadme && <div className={styles.readmecontainer}>
          <ReactMarkdown
            key={markdownKey}
            children={typedReadme}
            components={{
              code({node, inline, className, children, ...props}) {
                const match = /language-(\w+)/.exec(className || '')
                return !inline && match ? (
                  <SyntaxHighlighter
                    children={String(children).replace(/\n$/, '')}
                    language={match[1]}
                    PreTag="div"
                    {...props}
                  />
                ) : (
                  <code className={className} {...props}>
                    {children}
                  </code>
                )
              }
            }}
          />
        </div>}
        {readme && (
        <div className={styles.inputWrapper}>
          <input
            className={styles.chatcontainer}
            type="text"
            placeholder="Type changes here..."
            value={update} 
            onChange={(e) => setUpdate(e.target.value)}
          />
          <button className={styles.sendButton} onClick={handleChanges}>
            <FontAwesomeIcon icon={faPaperPlane} />
          </button>
        </div>
      )}
        {readme && (
        <div className={styles.buttonContainer}>
          <button onClick={handlePullRequest}>Create Pull Request</button>
          <button
            className={link ? styles.viewPRButton : styles.viewPRButtonDisabled}
            onClick={() => {
              if (link) window.open(link, '_blank', 'noopener noreferrer');
            }}
          >
            View Pull Request{' '}
            <FontAwesomeIcon icon={faExternalLinkAlt} />
          </button>
        </div>
        )}
      </div>
    </div>
  );
};

export default Hero;