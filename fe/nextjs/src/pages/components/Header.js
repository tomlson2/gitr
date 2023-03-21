import Link from 'next/link';
import styles from './Header.module.css';

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

      <Link href="https://gitr.herokuapp.com/login">
        <a className={styles.loginButton}>Login</a>
      </Link>
    </header>
  );
};

export default Header;
