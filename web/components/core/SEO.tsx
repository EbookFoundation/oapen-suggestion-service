import { APP_NAME_TEXT, APP_DESCRIPTION } from "../../constants";
import Head from "next/head";

interface SEOComponents {
  title?: string;
  description?: string;
}

export const SEO = ({ title, description }: SEOComponents) => {
  return (
    <Head>
      <title>
        {APP_NAME_TEXT} | {title}
      </title>
      <meta name="description" content={description || APP_DESCRIPTION} />
    </Head>
  );
};
