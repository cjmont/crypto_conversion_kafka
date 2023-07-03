import React, { useState, useEffect } from "react";

function useStatus() {
  const [error, setError] = useState(null);
  const [time, setTime] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    fetch("/api/test/status")
      .then((res) => {
        console.debug(res);
        return res.json();
      })
      .then(
        (data) => {
          setIsLoaded(true);
          setTime(data.data);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
      .catch((e) => {
        setIsLoaded(true);
        setError(e);
      });
  }, []);

  return {
    isLoaded,
    time,
    error,
  };
}

export default useStatus;
