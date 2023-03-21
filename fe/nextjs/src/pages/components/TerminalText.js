import './TerminalText.module.css';

function TerminalText({ text }) {
  return (
    <div>
      <span>{text}</span>
      <span className="terminal-cursor"></span>
    </div>
  );
}

export default TerminalText;
