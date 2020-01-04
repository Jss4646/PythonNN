const networkJSON = network.apiNetwork.layers;

fetch(`${window.origin}/set-cookie`, {
    method: "POST",
   credentials: "include",
   body: JSON.stringify(networkJSON),
   cache: "no-cache",
   headers: new Headers({
       "content-type": "application/json"
   })
});