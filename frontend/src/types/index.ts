export interface WebSocketMessage {
  type: string;
  payload: any;
  song: Song;
}

export interface Song {
  id: string;
  name: string;
  artist: string;
  url: string;
  albumArt: string | null;
  album: string;
  duration: number;
  emotion: string;
  lyrics: string[];
}
