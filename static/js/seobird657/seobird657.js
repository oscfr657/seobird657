
function shareToMastodon(link) {
    let shareInfo = link.dataset.shareInfo;
    let prompt = "Mastodon instance?";
    let instance = window.prompt(prompt);
    link.href = 'https:\/\/' + instance + '/share?text=' + shareInfo;
}
