import Link from 'next/link';
import styles from './Header.module.css';


  function getCookie(name) {
    if (typeof window !== 'undefined') {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    }
  }
  
  const userLogin = getCookie('userLogin');

const Header = () => {
  return (
    <header className={styles.header}>
      <Link href="/">
        <a>
          <div className={styles.logoContainer}>
            <img src="/logo.svg" alt="Documatic Logo" className={styles.logo} />
            <h1 className={styles.logoText}>gitr</h1>
          </div>
        </a>
      </Link>

      {!userLogin &&
      <Link href="https://gitr.herokuapp.com/login">
        <a className={styles.loginButton}>Login</a>
      </Link>
      }
      {userLogin &&
      <p className={styles.p}>Hello, {userLogin}</p>
      }
    </header>
  );
};

export default Header;
