import yt_dlp
import re
from typing import List, Dict, Optional


class MusicSearcher:
    def __init__(self):
        self.last_results = []
    
    def clean_query(self, query: str) -> str:
        query = re.sub(r'[^\w\s\-\'\"]+', ' ', query)
        query = ' '.join(query.split())
        return query
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        cleaned_query = self.clean_query(query)
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'dump_single_json': True,
            'default_search': 'ytsearch' + str(limit),
        }
        
        all_results = []
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                search_url = f"ytsearch{limit}:{cleaned_query}"
                search_results = ydl.extract_info(search_url, download=False)
                
                if search_results and 'entries' in search_results:
                    for entry in search_results['entries']:
                        if entry and len(all_results) < limit:
                            duration_sec = entry.get('duration', 0)
                            
                            if duration_sec:
                                hours = int(duration_sec // 3600)
                                minutes = int((duration_sec % 3600) // 60)
                                seconds = int(duration_sec % 60)
                                
                                if hours > 0:
                                    duration_str = f"{hours}:{minutes:02d}:{seconds:02d}"
                                else:
                                    duration_str = f"{minutes}:{seconds:02d}"
                            else:
                                duration_str = "Unknown"
                            
                            view_count = entry.get('view_count', 0)
                            if view_count:
                                if view_count >= 1000000:
                                    views_str = f"{view_count/1000000:.1f}M views"
                                elif view_count >= 1000:
                                    views_str = f"{view_count/1000:.1f}K views"
                                else:
                                    views_str = f"{view_count} views"
                            else:
                                views_str = "Unknown"
                            
                            if self._is_likely_music(entry, duration_sec):
                                all_results.append({
                                    'id': entry.get('id', ''),
                                    'title': entry.get('title', 'Unknown'),
                                    'channel': entry.get('uploader', 'Unknown'),
                                    'duration': duration_str,
                                    'views': views_str,
                                    'url': entry.get('url', f"https://youtube.com/watch?v={entry.get('id')}"),
                                    'thumbnail': entry.get('thumbnail', '')
                                })
        except Exception as e:
            print(f"Search error: {e}")
        
        self.last_results = all_results
        return all_results
    
    def _is_likely_music(self, entry: Dict, duration_sec: int) -> bool:
        title_lower = entry.get('title', '').lower()
        channel_lower = entry.get('uploader', '').lower()
        
        music_keywords = [
            'official', 'audio', 'lyrics', 'music', 'song', 'album',
            'vevo', 'records', 'entertainment', 'ft.', 'feat.'
        ]
        
        non_music_keywords = [
            'reaction', 'review', 'tutorial', '10 hours', '1 hour',
            'compilation', 'mix tape', 'playlist'
        ]
        
        has_music_keyword = any(keyword in title_lower or keyword in channel_lower 
                                for keyword in music_keywords)
        has_non_music_keyword = any(keyword in title_lower 
                                    for keyword in non_music_keywords)
        
        if duration_sec:
            total_minutes = duration_sec / 60
            if total_minutes > 20:
                return False
        
        if has_non_music_keyword and not has_music_keyword:
            return False
        
        return True
    
    def get_by_index(self, index: int) -> Optional[Dict]:
        if 0 <= index < len(self.last_results):
            return self.last_results[index]
        return None