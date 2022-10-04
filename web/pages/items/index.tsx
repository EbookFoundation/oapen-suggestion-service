import type { GetStaticProps } from "next";
import { OAPENItems } from "../../lib/oapen";
import type { OAPENItemQueried } from "../../lib/oapen/OAPENTypes";
import Link from "next/link";

interface ManyProps {
  many: OAPENItemQueried[];
}

export default function ItemMany({ many }: ManyProps) {
  return (
    <>
      <p>Hello</p>
      <h1>Listing</h1>
      <ul>
        {many.map((item) => (
          <li key={item.uuid}>
            <Link href={"/items/" + item.uuid}>
              <a>{item.name || item.uuid}</a>
            </Link>
          </li>
        ))}
      </ul>
    </>
  );
}

export const getStaticProps: GetStaticProps<ManyProps> = async (context) => {
  const many = await OAPENItems.getItemsRaw();
  const data: ManyProps = {
    many,
  };

  return {
    props: {
      ...data,
    },
  };
};
