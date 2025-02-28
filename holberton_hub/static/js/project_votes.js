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

function likeProject(projectId) {
    console.log("Sending like request for project:", projectId); // Debug log
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/projects/${projectId}/like/`, {  // Fixed URL path
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Received response:", data); // Debug log
        const likeButton = document.getElementById(`like-btn-${projectId}`);
        const likeCount = document.getElementById(`like-count-${projectId}`);

        if (data.liked) {
            likeButton.classList.add('liked');
        } else {
            likeButton.classList.remove('liked');
        }
        likeCount.textContent = data.count;
    })
    .catch(error => console.error('Error:', error));
}

function voteProject(projectId, voteType) {
    console.log("Sending vote request:", projectId, voteType); // Debug log
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/projects/${projectId}/vote/`, {  // Fixed URL path
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ vote_type: voteType })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const scoreElement = document.getElementById(`score-${projectId}`);
        scoreElement.textContent = data.score;

        const upvoteBtn = document.getElementById(`upvote-${projectId}`);
        const downvoteBtn = document.getElementById(`downvote-${projectId}`);

        if (voteType === 'up') {
            upvoteBtn.classList.toggle('active');
            downvoteBtn.classList.remove('active');
        } else if (voteType === 'down') {
            downvoteBtn.classList.toggle('active');
            upvoteBtn.classList.remove('active');
        }

        // Afficher un message de confirmation
        console.log(data.message);
    })
    .catch(error => console.error('Error:', error));
}
