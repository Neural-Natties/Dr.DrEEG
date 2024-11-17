export interface WebSocketMessage {
  emotion: string;
  song: Song;
  timestamp: number;
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
  lyrics?: string[];
}
