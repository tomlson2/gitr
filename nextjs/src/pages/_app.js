import '../styles/globals.css';

function MyApp({ Component, pageProps }) {
  return (
    <div style={{ backgroundColor: '#ffffff', minHeight: '100vh' }}>
      <Component {...pageProps} />
    </div>
  );
}

export default MyApp;
