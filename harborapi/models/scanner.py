# generated by datamodel-codegen:
#   filename:  scanner-adapter-openapi-v1.1.yaml
#   timestamp: 2022-07-04T09:31:34+00:00

from __future__ import annotations

from collections import Counter
from datetime import datetime
from enum import Enum
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Literal,
    NamedTuple,
    Optional,
    Tuple,
    Union,
    overload,
)

from pydantic import AnyUrl, BaseModel, Extra, Field


class SemVer(NamedTuple):
    # TODO: move this and get_version_tuple() to separate module (for reuse)
    major: int
    minor: int
    patch: int


class Scanner(BaseModel):
    name: Optional[str] = Field(
        None, description="The name of the scanner.", example="Trivy"
    )
    vendor: Optional[str] = Field(
        None, description="The name of the scanner's provider.", example="Aqua Security"
    )
    version: Optional[str] = Field(
        None, description="The version of the scanner.", example="0.4.0"
    )

    def get_version_tuple(self) -> SemVer:
        if self.version is None:
            return SemVer(0, 0, 0)
        parts = self.version.split(".")
        return SemVer(*[int(part) for part in parts])  # why have to wrap in list?


class ScannerProperties(BaseModel):
    pass

    class Config:
        extra = Extra.allow


class ScannerCapability(BaseModel):
    consumes_mime_types: List[str] = Field(
        ...,
        description='The set of MIME types of the artifacts supported by the scanner to produce the reports specified in the "produces_mime_types". A given\nmime type should only be present in one capability item.\n',
        example=[
            "application/vnd.oci.image.manifest.v1+json",
            "application/vnd.docker.distribution.manifest.v2+json",
        ],
    )
    produces_mime_types: List[str] = Field(
        ...,
        description="The set of MIME types of reports generated by the scanner for the consumes_mime_types of the same capability record.\n",
        example=[
            "application/vnd.scanner.adapter.vuln.report.harbor+json; version=1.0"
        ],
    )


class ScanRequestId(BaseModel):
    __root__: str = Field(
        ...,
        description="A unique identifier returned by the [/scan](#/operation/AcceptScanRequest] operations. The format of the\nidentifier is not imposed but it should be unique enough to prevent collisons when polling for scan reports.\n",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa6",
    )


class Registry(BaseModel):
    url: Optional[str] = Field(
        None,
        description="A base URL or the Docker Registry v2 API.",
        example="https://core.harbor.domain",
    )
    authorization: Optional[str] = Field(
        None,
        description="An optional value of the HTTP Authorization header sent with each request to the Docker Registry v2 API.\nIt's used to exchange Base64 encoded robot account credentials to a short lived JWT access token which\nallows the underlying scanner to pull the artifact from the Docker Registry.\n",
        example="Basic BASE64_ENCODED_CREDENTIALS",
    )


class Artifact(BaseModel):
    repository: Optional[str] = Field(
        None,
        description="The name of the Docker Registry repository containing the artifact.",
        example="library/mongo",
    )
    digest: Optional[str] = Field(
        None,
        description="The artifact's digest, consisting of an algorithm and hex portion.",
        example="sha256:6c3c624b58dbbcd3c0dd82b4c53f04194d1247c6eebdaab7c610cf7d66709b3b",
    )
    tag: Optional[str] = Field(
        None, description="The artifact's tag", example="3.14-xenial"
    )
    mime_type: Optional[str] = Field(
        None,
        description="The MIME type of the artifact.",
        example="application/vnd.docker.distribution.manifest.v2+json",
    )


class Severity(Enum):
    unknown = "Unknown"
    negligible = "Negligible"
    low = "Low"
    medium = "Medium"
    high = "High"
    critical = "Critical"


class Error(BaseModel):
    message: Optional[str] = Field(None, example="Some unexpected error")


class CVSSDetails(BaseModel):
    score_v3: Optional[float] = Field(
        None, description="The CVSS 3.0 score for the vulnerability.\n", example=3.2
    )
    score_v2: Optional[float] = Field(
        None, description="The CVSS 2.0 score for the vulnerability.\n"
    )
    vector_v3: Optional[str] = Field(
        None,
        description="The CVSS 3.0 vector for the vulnerability. \n",
        example="CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N",
    )
    vector_v2: Optional[str] = Field(
        None,
        description="The CVSS 2.0 vector for the vulnerability. The string is of the form AV:L/AC:M/Au:N/C:P/I:N/A:N\n",
        example="AV:N/AC:L/Au:N/C:N/I:N/A:P",
    )


class ScannerAdapterMetadata(BaseModel):
    scanner: Scanner
    capabilities: List[ScannerCapability]
    properties: Optional[ScannerProperties] = None


class ScanRequest(BaseModel):
    registry: Registry
    artifact: Artifact


class ScanResponse(BaseModel):
    id: ScanRequestId


class VulnerabilityItem(BaseModel):
    id: Optional[str] = Field(
        None,
        description="The unique identifier of the vulnerability.",
        example="CVE-2017-8283",
    )
    package: Optional[str] = Field(
        None,
        description="An operating system package containing the vulnerability.\n",
        example="dpkg",
    )
    version: Optional[str] = Field(
        None,
        description="The version of the package containing the vulnerability.\n",
        example="1.17.27",
    )
    fix_version: Optional[str] = Field(
        None,
        description="The version of the package containing the fix if available.\n",
        example="1.18.0",
    )
    severity: Optional[Severity] = None
    description: Optional[str] = Field(
        None,
        description="The detailed description of the vulnerability.\n",
        example="dpkg-source in dpkg 1.3.0 through 1.18.23 is able to use a non-GNU patch program\nand does not offer a protection mechanism for blank-indented diff hunks, which\nallows remote attackers to conduct directory traversal attacks via a crafted\nDebian source package, as demonstrated by using of dpkg-source on NetBSD.\n",
    )
    links: Optional[List[AnyUrl]] = Field(
        None,
        description="The list of links to the upstream databases with the full description of the vulnerability.\n",
        example=["https://security-tracker.debian.org/tracker/CVE-2017-8283"],
    )
    preferred_cvss: Optional[CVSSDetails] = None
    cwe_ids: Optional[List[str]] = Field(
        None,
        description="The Common Weakness Enumeration Identifiers associated with this vulnerability.\n",
        example=["CWE-476"],
    )
    vendor_attributes: Optional[Dict[str, Any]] = None

    @property
    def fixable(self) -> bool:
        return self.fix_version is not None

    def get_cvss_score(
        self,
        scanner: Optional[Scanner],
        version: int = 3,
        vendor_priority: Iterable[str] = ("nvd", "redhat"),
        default: float = 0.0,
    ) -> float:
        """The default scanner Trivy, as of version 0.29.1, does not use the
        preferred_cvss field.

        In order to not tightly couple this method with a specific scanner,
        we use the scanner name to determinehow to retrieve the CVSS score.

        Forward compatibility is in place in the event that Trivy starts
        conforming to the spec.
        """
        # Forward compatibility for Trivy (and others):
        # try to use the preferred_cvss field first in case it is implemented in the future
        if self.preferred_cvss is not None:
            if version == 3 and self.preferred_cvss.score_v3 is not None:
                return self.preferred_cvss.score_v3
            elif version == 2 and self.preferred_cvss.score_v2 is not None:
                return self.preferred_cvss.score_v2

        # fallback to the scanner-specific CVSS score
        # TODO: refactor: move to a separate function
        if not scanner:
            return default

        if scanner.name == "Trivy":
            if self.vendor_attributes is None:
                return default

            cvss_data = self.vendor_attributes.get("CVSS")
            if not cvss_data:
                return default

            for prio in vendor_priority:
                # Trivy uses the vendor name as the key for the CVSS data
                vendor_cvss = cvss_data.get(prio)
                if vendor_cvss is None:
                    continue
                # NOTE: we can't guarantee these values are floats (dangerous)
                if version == 3:
                    return vendor_cvss.get("V3Score")
                elif version == 2:
                    return vendor_cvss.get("V2Score")

        # Other scanners here
        # ...

        return default


class ErrorResponse(BaseModel):
    error: Optional[Error] = None


class HarborVulnerabilityReport(BaseModel):
    generated_at: Optional[datetime] = Field(
        None, description="The time the report was generated."
    )
    artifact: Optional[Artifact] = Field(None, description="The artifact scanned.")
    scanner: Optional[Scanner] = Field(
        None, description="The scanner used to generate the report."
    )
    # Changes from spec: these two fields have been given defaults
    # TODO: document this
    severity: Severity = Field(
        Severity.unknown, description="The overall severity of the vulnerabilities."
    )
    vulnerabilities: List[VulnerabilityItem] = Field(
        default_factory=list, description="The list of vulnerabilities found."
    )

    def __repr__(self) -> str:
        return f"HarborVulnerabilityReport(generated_at={self.generated_at}, artifact={self.artifact}, scanner={self.scanner}, severity={self.severity}, vulnerabilities=list(len={len(self.vulnerabilities)}))"

    @property
    def fixable(self) -> List[VulnerabilityItem]:
        return [v for v in self.vulnerabilities if v.fixable]

    @property
    def unfixable(self) -> List[VulnerabilityItem]:
        return [v for v in self.vulnerabilities if not v.fixable]

    @property
    def critical(self) -> List[VulnerabilityItem]:
        return self.vulnerabilities_by_severity(Severity.critical)

    @property
    def high(self) -> List[VulnerabilityItem]:
        return self.vulnerabilities_by_severity(Severity.high)

    @property
    def medium(self) -> List[VulnerabilityItem]:
        return self.vulnerabilities_by_severity(Severity.medium)

    @property
    def low(self) -> List[VulnerabilityItem]:
        return self.vulnerabilities_by_severity(Severity.low)

    @property
    def distribution(self) -> Counter[Severity]:
        dist = Counter()  # type: Counter[Severity]
        for vulnerability in self.vulnerabilities:
            if vulnerability.severity:
                dist[vulnerability.severity] += 1
        return dist

    def vulnerabilities_by_severity(
        self, severity: Severity
    ) -> List[VulnerabilityItem]:
        return [v for v in self.vulnerabilities if v.severity == severity]

    @property
    def cvss_scores(self) -> List[float]:
        """Returns a list of CVSS scores for each vulnerability.
        Vulnerabilities with a score of `None` are omitted.

        Returns
        ----
        List[Optional[float]]
            A list of CVSS scores for each vulnerability.
        """
        return list(
            filter(
                None.__ne__,  # type: ignore
                [v.get_cvss_score(self.scanner) for v in self.vulnerabilities],  # type: ignore
            )
        )

    def top_vulns(self, n: int = 5, fixable: bool = False) -> List[VulnerabilityItem]:
        """Returns the n most severe vulnerabilities.


        Parameters
        ----------
        n : int
            The maximum number of vulnerabilities to return.
        fixable : bool
            If `True`, only vulnerabilities with a fix version are returned.

        Returns
        -------
        List[VulnerabilityItem]
            The n most severe vulnerabilities.

        """
        # TODO: implement UNfixable
        if fixable:
            vulns = self.fixable
        else:
            vulns = self.vulnerabilities
        return sorted(
            vulns, key=lambda v: v.get_cvss_score(self.scanner), reverse=True
        )[:n]
