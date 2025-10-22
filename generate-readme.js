const fs = require('fs');
const axios = require('axios');

const username = 'YOUR_GITHUB_USERNAME'; // Replace with your GitHub username
const readmePath = './README.md';

async function fetchRepos() {
    const res = await axios.get(`https://api.github.com/users/${username}/repos?sort=updated&per_page=100`);
    return res.data;
}

function generateTable(repos) {
    let table = `| Name | Description | Language | Updated |\n| --- | --- | --- | --- |\n`;
    repos.forEach(repo => {
        table += `| [${repo.name}](${repo.html_url}) | ${repo.description || ''} | ${repo.language || ''} | ${new Date(repo.updated_at).toLocaleDateString()} |\n`;
    });
    return table;
}

async function main() {
    const repos = await fetchRepos();
    let readme = fs.readFileSync(readmePath, 'utf8');

    const startTag = '<!-- REPO_TABLE_START -->';
    const endTag = '<!-- REPO_TABLE_END -->';

    const table = generateTable(repos);

    if (readme.includes(startTag) && readme.includes(endTag)) {
        const newReadme = readme.replace(
            new RegExp(`${startTag}[\\s\\S]*?${endTag}`, 'm'),
            `${startTag}\n${table}${endTag}`
        );
        fs.writeFileSync(readmePath, newReadme);
    } else {
        // If tags not found, append table at the end
        fs.appendFileSync(readmePath, `\n${startTag}\n${table}${endTag}\n`);
    }

    console.log('README updated with latest repos!');
}

main();
