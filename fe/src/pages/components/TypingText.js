import React from 'react';
import useTypewriter from '../hooks/useTypewriter';

const TypingText = ({ textToType, typingSpeed }) => {
  const typedText = useTypewriter(textToType, typingSpeed);

  React.useEffect(() => {
    console.log('Typed text:', typedText);
  }, [typedText]);

  return <p>{typedText}</p>;
};

export default TypingText;