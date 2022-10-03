import type { GetStaticProps } from "next";

interface SingleItemProps {
  uuid: string;
}

export const SingleItem = ({ uuid }: SingleItemProps) => {
  return (
    <>
      <h1>{uuid}</h1>
    </>
  );
};

export const getStaticProps: GetStaticProps<SingleItemProps> = async (
  context
) => {
  const data: SingleItemProps = {
    uuid: context.params?.uuid,
  };

  return {
    props: {
      ...data,
    },
  };
};
