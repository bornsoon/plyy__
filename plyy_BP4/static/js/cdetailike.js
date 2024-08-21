function CdetailToggleLike(u_id, cid) {
    const likeButton = document.getElementById(`like-${cid}`);
    const method = curatorLikeStates[cid] ? 'DELETE' : 'POST';
    const url = curatorLikeStates[cid] ? `/plyy/api/unlike/${encodeURIComponent(u_id)}/${encodeURIComponent(cid)}` : `/plyy/api/like/${encodeURIComponent(u_id)}/${encodeURIComponent(cid)}`;

    fetch(url, { method: method })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                curatorLikeStates[cid] = !curatorLikeStates[cid]; // 좋아요 상태 토글
                if (curatorLikeStates[cid]) {
                    likeButton.classList.remove('btn-curator-heart--unfill');
                    likeButton.classList.add('btn-curator-heart--fill');
                } else {
                    likeButton.classList.remove('btn-curator-heart--fill');
                    likeButton.classList.add('btn-curator-heart--unfill');
                }
            } else {
                console.error('Failed to toggle like:', data.error);
            }
        })
        .catch(error => {
            console.error('Error toggling like:', error);
        });
}
