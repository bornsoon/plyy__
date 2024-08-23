function PlaylistToggleLike(u_id, pid) {
    const likeButton = document.getElementById(`like-${pid}`);
    const method = playlistLikeStates[pid] ? 'DELETE' : 'POST';
    const url = playlistLikeStates[pid] ? `/plyy/api/plyyunlike/${encodeURIComponent(u_id)}/${encodeURIComponent(pid)}` : `/plyy/api/plyylike/${encodeURIComponent(u_id)}/${encodeURIComponent(pid)}`;

    fetch(url, { method: method })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                playlistLikeStates[pid] = !playlistLikeStates[pid]; // 좋아요 상태 토글
                if (playlistLikeStates[pid]) {
                    likeButton.classList.remove('btn-plike--unfill');
                    likeButton.classList.add('btn-plike--fill');
                } else {
                    likeButton.classList.remove('btn-plike--fill');
                    likeButton.classList.add('btn-plike--unfill');
                }
            } else {
                console.error('Failed to toggle like:', data.error);
            }
        })
        .catch(error => {
            console.error('Error toggling like:', error);
        });
}