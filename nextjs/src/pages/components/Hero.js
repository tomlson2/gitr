import { useState } from 'react';
import styles from './Hero.module.css';
import ReactMarkdown from 'react-markdown';
import {Prism as SyntaxHighlighter} from 'react-syntax-highlighter';
import useTypewriter from '../hooks/useTypewriter';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faExternalLinkAlt } from '@fortawesome/free-solid-svg-icons';
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';

const Hero = () => {
  const [readme, setReadme] = useState('');
  const [username, setUsername] = useState('');
  const [repo, setRepo] = useState('');
  const [generating, startedGenerating] = useState(false);
  const [link, setLink] = useState('');

  const handleGenerateReadme = async () => {
    startedGenerating(true);
    const res = await fetch(`http://localhost:5000/api/readme?username=${username}&repo=${repo}`);
    const data = await res.json();
    startedGenerating(false);
    setReadme(data.readme);
  };
  
  const handlePullRequest = async () => {
    const res = await fetch(`http://localhost:5000/api/pr?username=${username}&repo=${repo}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ readme })
    });
    const data = await res.json();
    setLink(data.link);
  };

  const handleChanges = async () => {
    return null;
  }

  const typedReadme = useTypewriter(readme, 5);
  
  return (
    <div className={styles.hero}>
      <div className={styles.content}>
        <h1>WRITEME.md</h1>
        <p>Automatically generate READMEs for your GitHub repositories</p>
        <div className={styles.inputcontainer}>
          <input type="text" placeholder="GitHub Username" value={username} onChange={(e) => setUsername(e.target.value)} />
          <input type="text" placeholder="Repository Name" value={repo} onChange={(e) => setRepo(e.target.value)} />
          <button onClick={handleGenerateReadme}>Generate README</button>
        </div>
        {generating && <div className={styles.readmecontainer}>
          <span className={styles.cursor}></span>
        </div>}
        {readme && <div className={styles.readmecontainer}>
          <ReactMarkdown
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