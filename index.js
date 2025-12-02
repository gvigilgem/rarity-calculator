export default {
  async fetch(request) {
    return new Response("FBI Access Portal - Live", {
      headers: { "content-type": "text/plain" },
    });
  },
};