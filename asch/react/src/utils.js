

export function build_request(request_string) {
    return `${window.location.protocol}//${window.location.host}${request_string}`
}
