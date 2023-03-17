import { useState } from 'react';
import styles from './Hero.module.css';
import ReactMarkdown from 'react-markdown';
import {Prism as SyntaxHighlighter} from 'react-syntax-highlighter';
import useTypewriter from '../hooks/useTypewriter';
import TerminalText from './TerminalText';

const Hero = () => {
  const [readme, setReadme] = useState('');
  const [username, setUsername] = useState('');
  const [repo, setRepo] = useState('');
  const [generating, startedGenerating] = useState(false);

  const handleGenerateReadme = async () => {
    startedGenerating(true);
    const res = await fetch(`http://localhost:5000/api/readme?username=${username}&repo=${repo}`);
    const data = await res.json();
    startedGenerating(false);
    setReadme(data.readme);
  };

  const typedReadme = useTypewriter(readme, 10);
  
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
          <span class={styles.cursor}></span>
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
        {readme && <input className={styles.chatcontainer} type="text" placeholder="Type changes here..."/>}
      </div>
    </div>
  );
};

export default Hero;