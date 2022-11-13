export const getWaitingTime = () => {
    var result;
    const url = "http://127.0.0.1:5000/dummy";
    // fetch(url)
    //     .then((response) => response.json())
    //     .then((json) => result = json['results'])
    //     .catch((error) => console.log(error));
    result = [
        {"lat":37.7739233, "long":-122.4373049, "wait":1.0},
        {"lat":37.7737809, "long":122.437817, "wait":1.5},
        {"lat":37.7734016, "long":-122.4371386, "wait":15},
];
    console.log(result);
    return result;
}