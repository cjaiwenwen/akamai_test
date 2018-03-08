provider "akamai" {
    edgerc = "/var/jenkins_home/workspace/akamai_test/.edgerc"
    papi_section = "papi"
}

resource "akamai_property" "junchen_sandbox" {
}
