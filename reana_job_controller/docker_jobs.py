# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2018 CERN.
#
# REANA is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# REANA is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# REANA; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization or
# submit itself to any jurisdiction.

"""Docker job controller."""

import logging

import docker


def instantiate_docker_job(job_id, docker_img, cmd, cvmfs_repos, env_vars,
                           namespace, shared_file_system):
    """Create docker job.

    :param job_id: Job uuid.
    :param docker_img: Docker image to run the job.
    :param cmd: Command provided to the docker container.
    :param cvmfs_repos: List of CVMFS repository names.
    :param env_vars: Dictionary representing environment variables
        as {'var_name': 'var_value'}.
    :param namespace: Job's namespace.
    :shared_file_system: Boolean which represents whether the job
        should have a shared file system mounted.
    :returns: Docker job object if the job was successfuly created,
        None if not.
    """
    client = docker.from_env()
    if cmd:
        import shlex
        command = shlex.split(cmd)
    container = client.containers.run(docker_img,
                                      command=command,
                                      environment=env_vars,
                                      auto_remove=True,
                                      detach=True)
    return container


def watch_docker_jobs(job_db, config):
    """Return the status of a docker job."""
    client = docker.from_env()
    while True:
        logging.debug('Watching all running docker jobs.')
        for log in client.containers.logs(**config):
            print(log)