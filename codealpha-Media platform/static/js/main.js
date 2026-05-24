function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function likePost(postId) {
    fetch(`/post/${postId}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        const postCard = document.getElementById(`post-${postId}`);
        const likeItem = postCard.querySelector('.action-item');
        const likeIcon = likeItem.querySelector('i');
        const likeCount = likeItem.querySelector('.like-count');

        if (data.liked) {
            likeItem.classList.add('liked');
            likeIcon.classList.remove('far');
            likeIcon.classList.add('fas');
        } else {
            likeItem.classList.remove('liked');
            likeIcon.classList.remove('fas');
            likeIcon.classList.add('far');
        }
        likeCount.innerText = data.count;
    });
}

function toggleComments(postId) {
    const section = document.getElementById(`comments-${postId}`);
    section.classList.toggle('hidden');
}

function addComment(postId) {
    const input = document.getElementById(`input-${postId}`);
    const text = input.value;
    if (!text) return;

    const formData = new FormData();
    formData.append('text', text);

    fetch(`/post/${postId}/comment/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            const list = document.getElementById(`list-${postId}`);
            const commentDiv = document.createElement('div');
            commentDiv.className = 'comment-entry';
            commentDiv.innerHTML = `<span class="comment-username">${data.author}</span>: ${data.text}`;
            list.appendChild(commentDiv);
            input.value = '';
        }
    });
}
