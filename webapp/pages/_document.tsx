import Document, { Html, Head, Main, NextScript } from 'next/document';
import Script from "next/script";

class MyDocument extends Document {
  render() {
    return (
      <Html>
        <Head>
          <Script
            src="https://telegram.org/js/telegram-web-app.js"
            strategy="beforeInteractive"
          />  
          {/* Other head elements */}
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}

export default MyDocument;
