import Link from 'next/link';
import styles from './Header.module.css';

const Header = () => {
  return (
    <header className={styles.header}>
      <Link href="/">
        <div className={styles.logoContainer}>
          <img src="/logo.svg" alt="Documatic Logo" className={styles.logo} />
          <h1 className={styles.logoText}>Documatic</h1>
        </div>
      </Link>
    </header>
  );
};

export default Header;
