const API_BASE_URL = "http://localhost:5000";

export const generateReadme = async (repo) => {
  const res = await fetch(`${API_BASE_URL}/api/readme?repo=${repo}`, {
    method: 'GET',
    credentials: 'include'
  });
  const data = await res.json();
  return data.readme;
};

export const createPullRequest = async (repo, readme) => {
  const res = await fetch(`${API_BASE_URL}/api/pr?repo=${repo}`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ readme })
  });
  const data = await res.json();
  return data.link;
};

export const updateReadme = async (readme, update) => {
  const res = await fetch(`${API_BASE_URL}/api/update-readme`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ readme, update })
  });
  const data = await res.json();
  return data.readme;
};