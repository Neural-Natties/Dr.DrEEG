import { useEffect, useState } from 'react';

export const useSpotifyAuth = () => {
  let [token, setToken] = useState<string | null>(null);

  fetch(`http://localhost:8000/auth/token`)
        .then((res) => res.json())
        .then((data) => setToken(data.access_token))

  return { token };
};
