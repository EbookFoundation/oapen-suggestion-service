import styles from "./index.module.css";
import { SEO } from "../components/core";
export default function Home() {
  return (
    <div className={styles.container}>
      <SEO title={"Home"} />

      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to the OAPEN Suggestion Service
        </h1>
      </main>
    </div>
  );
}
