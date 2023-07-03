import type { NextPage } from "next";
import useStatus from "../hooks/status.hook";

const Home: NextPage = () => {
  const { time, error, isLoaded } = useStatus();
  if (error) {
    return <div>Error: {error.toString()}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  } else {
    return <div>Hello NotBank {time}</div>;
  }
};

export default Home;
