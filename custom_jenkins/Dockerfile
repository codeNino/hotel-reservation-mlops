FROM jenkins/jenkins:lts

USER root

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        apt-transport-https ca-certificates curl gnupg lsb-release && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
        https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
        > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends docker-ce docker-ce-cli containerd.io && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN groupadd -f docker && usermod -aG docker jenkins

USER jenkins
