import React, { useState, useEffect } from 'react';

const useTypewriter = (textToType, typingSpeed) => {
  const [typedText, setTypedText] = useState('');

  useEffect(() => {
    setTypedText(''); // Reset the typed text when the textToType changes
    let index = 0;
    let typingTimeout;

    const typeText = () => {
      if (index <= textToType.length) {
        setTypedText(textToType.slice(0, index));
        index++;
        typingTimeout = setTimeout(typeText, typingSpeed);
      }
    };

    typeText();

    return () => {
      clearTimeout(typingTimeout); // Properly clear the timeout when the effect is cleaned up
    };
  }, [textToType, typingSpeed]);

  return typedText;
};

export default useTypewriter;