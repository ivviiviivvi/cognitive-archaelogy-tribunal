"""
Metadata utilities for Cognitive Archaeology Tribunal
Implements governance standards for IDs, metadata, provenance tracking
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import json


class MetadataGenerator:
    """Generate standard metadata for all outputs."""

    SCHEMA_VERSION = "1.0.0"
    TOOL_NAME = "cognitive-tribunal"
    TOOL_VERSION = "0.2.0"

    @staticmethod
    def generate_uuid() -> str:
        """Generate RFC 4122 compliant UUID."""
        return f"uuid:{uuid.uuid4()}"

    @staticmethod
    def timestamp() -> str:
        """Generate ISO 8601 timestamp in UTC."""
        return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    @classmethod
    def base_metadata(
        cls,
        data_type: str,
        module_name: str,
        source_files: Optional[List[str]] = None,
        version: str = "1.0.0",
        license_: str = "CC0-1.0",
        attribution: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate base metadata structure for outputs.

        Args:
            data_type: Type of data (ai-conversations, archives, etc.)
            module_name: Name of the module that generated the data
            source_files: List of source file paths
            version: Dataset version (semantic versioning)
            license_: SPDX license identifier
            attribution: Optional attribution text

        Returns:
            Standard metadata dictionary
        """
        now = cls.timestamp()

        return {
            "metadata": {
                "id": cls.generate_uuid(),
                "type": data_type,
                "version": version,
                "schema_version": cls.SCHEMA_VERSION,
                "created_at": now,
                "updated_at": now,
                "generator": {
                    "tool": cls.TOOL_NAME,
                    "version": cls.TOOL_VERSION,
                    "module": module_name
                },
                "provenance": {
                    "source_files": source_files or [],
                    "processing_date": now,
                    "parameters": {}
                },
                "license": license_,
                "attribution": attribution
            }
        }

    @classmethod
    def add_dublin_core(
        cls,
        metadata: Dict[str, Any],
        title: str,
        creator: str,
        description: str,
        subjects: Optional[List[str]] = None,
        coverage: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add Dublin Core metadata elements.

        Args:
            metadata: Existing metadata dict
            title: Dataset title
            creator: Creator/author name
            description: Dataset description
            subjects: List of subject keywords
            coverage: Temporal or spatial coverage

        Returns:
            Metadata with Dublin Core added
        """
        metadata["metadata"]["dublin_core"] = {
            "dc:title": title,
            "dc:creator": creator,
            "dc:subject": subjects or [],
            "dc:description": description,
            "dc:publisher": "Cognitive Archaeology Tribunal",
            "dc:date": datetime.now(timezone.utc).date().isoformat(),
            "dc:type": "Dataset",
            "dc:format": "application/json",
            "dc:identifier": metadata["metadata"]["id"],
            "dc:language": "en",
            "dc:rights": metadata["metadata"]["license"]
        }

        if coverage:
            metadata["metadata"]["dublin_core"]["dc:coverage"] = coverage

        return metadata

    @classmethod
    def add_datacite(
        cls,
        metadata: Dict[str, Any],
        creators: List[Dict[str, str]],
        doi: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add DataCite schema metadata for DOI registration.

        Args:
            metadata: Existing metadata dict
            creators: List of creator dicts with 'name' and optional 'orcid'
            doi: DOI if already registered

        Returns:
            Metadata with DataCite schema added
        """
        title = metadata["metadata"].get("dublin_core", {}).get("dc:title", "Untitled Dataset")
        subjects = metadata["metadata"].get("dublin_core", {}).get("dc:subject", [])

        metadata["metadata"]["datacite"] = {
            "identifier": doi or metadata["metadata"]["id"],
            "identifierType": "DOI" if doi else "UUID",
            "creators": creators,
            "titles": [{"title": title}],
            "publisher": "Cognitive Archaeology Tribunal",
            "publicationYear": str(datetime.now(timezone.utc).year),
            "resourceType": "Dataset",
            "subjects": subjects,
            "dates": [
                {
                    "date": metadata["metadata"]["created_at"],
                    "dateType": "Created"
                }
            ],
            "version": metadata["metadata"]["version"],
            "rights": [
                {
                    "rights": metadata["metadata"]["license"],
                    "rightsURI": cls._license_uri(metadata["metadata"]["license"])
                }
            ]
        }

        return metadata

    @staticmethod
    def _license_uri(spdx_id: str) -> str:
        """Get license URI from SPDX identifier."""
        license_uris = {
            "CC0-1.0": "https://creativecommons.org/publicdomain/zero/1.0/",
            "CC-BY-4.0": "https://creativecommons.org/licenses/by/4.0/",
            "CC-BY-SA-4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
            "CC-BY-NC-4.0": "https://creativecommons.org/licenses/by-nc/4.0/",
            "MIT": "https://opensource.org/licenses/MIT",
            "ODbL-1.0": "https://opendatacommons.org/licenses/odbl/1-0/"
        }
        return license_uris.get(spdx_id, "")

    @classmethod
    def wrap_data(
        cls,
        data: Any,
        data_type: str,
        module_name: str,
        title: str,
        creator: str,
        description: str,
        source_files: Optional[List[str]] = None,
        version: str = "1.0.0",
        license_: str = "CC0-1.0",
        subjects: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Wrap data with complete metadata.

        Args:
            data: The actual data to wrap
            data_type: Type of data
            module_name: Module that generated it
            title: Dataset title
            creator: Creator name
            description: Description
            source_files: Source file paths
            version: Dataset version
            license_: SPDX license ID
            subjects: Subject keywords

        Returns:
            Complete output with metadata and data
        """
        # Base metadata
        output = cls.base_metadata(
            data_type=data_type,
            module_name=module_name,
            source_files=source_files,
            version=version,
            license_=license_
        )

        # Dublin Core
        output = cls.add_dublin_core(
            metadata=output,
            title=title,
            creator=creator,
            description=description,
            subjects=subjects
        )

        # Add data
        output["data"] = data

        return output

    @classmethod
    def update_timestamp(cls, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Update the updated_at timestamp."""
        if "metadata" in metadata:
            metadata["metadata"]["updated_at"] = cls.timestamp()
        return metadata

    @classmethod
    def add_processing_step(
        cls,
        metadata: Dict[str, Any],
        step: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add a processing step to provenance.

        Args:
            metadata: Metadata dict
            step: Name of processing step
            parameters: Parameters used in this step

        Returns:
            Updated metadata
        """
        if "metadata" in metadata and "provenance" in metadata["metadata"]:
            if "processing_steps" not in metadata["metadata"]["provenance"]:
                metadata["metadata"]["provenance"]["processing_steps"] = []

            metadata["metadata"]["provenance"]["processing_steps"].append({
                "step": step,
                "timestamp": cls.timestamp(),
                "parameters": parameters or {}
            })

        return metadata


class CitationGenerator:
    """Generate citations for datasets."""

    @staticmethod
    def to_bibtex(
        dataset_id: str,
        author: str,
        title: str,
        year: str,
        version: str,
        doi: Optional[str] = None,
        url: Optional[str] = None
    ) -> str:
        """Generate BibTeX citation."""
        # Clean dataset ID for BibTeX key
        key = dataset_id.replace(":", "_").replace("-", "_")

        bibtex = f"""@dataset{{{key},
  author = {{{author}}},
  title = {{{title}}},
  year = {{{year}}},
  publisher = {{Cognitive Archaeology Tribunal}},
  version = {{{version}}}"""

        if doi:
            bibtex += f",\n  doi = {{{doi}}}"
        if url:
            bibtex += f",\n  url = {{{url}}}"

        bibtex += "\n}"

        return bibtex

    @staticmethod
    def to_apa(
        author: str,
        year: str,
        title: str,
        version: str,
        doi: Optional[str] = None,
        url: Optional[str] = None
    ) -> str:
        """Generate APA style citation."""
        citation = f"{author}. ({year}). {title} (Version {version}) [Data set]. "
        citation += "Cognitive Archaeology Tribunal. "

        if doi:
            citation += f"https://doi.org/{doi}"
        elif url:
            citation += url

        return citation

    @staticmethod
    def to_chicago(
        author: str,
        year: str,
        title: str,
        version: str,
        doi: Optional[str] = None,
        url: Optional[str] = None
    ) -> str:
        """Generate Chicago style citation."""
        citation = f"{author}. {year}. \"{title}.\" Version {version}. "
        citation += "Cognitive Archaeology Tribunal. "

        if doi:
            citation += f"https://doi.org/{doi}."
        elif url:
            citation += f"{url}."

        return citation

    @classmethod
    def from_metadata(cls, metadata: Dict[str, Any], format_: str = "bibtex") -> str:
        """
        Generate citation from metadata dict.

        Args:
            metadata: Metadata dictionary
            format_: Citation format (bibtex, apa, chicago)

        Returns:
            Formatted citation string
        """
        meta = metadata.get("metadata", {})
        dc = meta.get("dublin_core", {})
        datacite = meta.get("datacite", {})

        dataset_id = meta.get("id", "unknown")
        author = dc.get("dc:creator", "Unknown")
        title = dc.get("dc:title", "Untitled Dataset")
        year = dc.get("dc:date", "")[:4] or str(datetime.now().year)
        version = meta.get("version", "1.0.0")
        doi = datacite.get("identifier") if datacite.get("identifierType") == "DOI" else None
        url = meta.get("url")

        if format_ == "bibtex":
            return cls.to_bibtex(dataset_id, author, title, year, version, doi, url)
        elif format_ == "apa":
            return cls.to_apa(author, year, title, version, doi, url)
        elif format_ == "chicago":
            return cls.to_chicago(author, year, title, version, doi, url)
        else:
            raise ValueError(f"Unknown citation format: {format_}")


if __name__ == "__main__":
    # Example usage
    mg = MetadataGenerator()

    # Create metadata for a dataset
    metadata = mg.wrap_data(
        data={"conversations": [], "stats": {}},
        data_type="ai-conversations",
        module_name="AIContextAggregator",
        title="My AI Conversations Dataset",
        creator="John Doe",
        description="Collection of ChatGPT conversations about cognitive archaeology",
        source_files=["conversations.json"],
        version="1.0.0",
        license_="CC0-1.0",
        subjects=["artificial intelligence", "conversations", "cognitive archaeology"]
    )

    # Add DataCite for DOI
    metadata = mg.add_datacite(
        metadata=metadata,
        creators=[{"name": "Doe, John", "orcid": "0000-0000-0000-0000"}],
        doi="10.5281/zenodo.1234567"
    )

    print(json.dumps(metadata, indent=2))

    # Generate citations
    cg = CitationGenerator()
    print("\nBibTeX:")
    print(cg.from_metadata(metadata, "bibtex"))
    print("\nAPA:")
    print(cg.from_metadata(metadata, "apa"))
    print("\nChicago:")
    print(cg.from_metadata(metadata, "chicago"))
