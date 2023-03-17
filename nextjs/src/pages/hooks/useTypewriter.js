import React, { useState, useEffect } from 'react';
import styles from '../../styles/Home.module.css'

const useTypewriter = (textToType, typingSpeed) => {
  const [typedText, setTypedText] = useState('');
  useEffect(() => {
    let index = 0;

    const typeText = () => {
      if (index <= textToType.length) {
        setTypedText(typedText + textToType.slice(0, index));
        index++;
        setTimeout(typeText, typingSpeed);
      }
    };

    typeText();

    return () => {
      clearTimeout(typeText);
    };
  }, [textToType, typingSpeed]);

  return typedText;
};

export default useTypewriter;