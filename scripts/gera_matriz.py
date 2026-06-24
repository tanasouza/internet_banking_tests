from pathlib import Path
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report.xml"

TRACEABILITY = {
    "test_transferencia_saldo_igual_valor": {
        "id": "TC-S1-001",
        "requirement": "REQ-TRF-001 - Transferir valor total disponivel quando ha saldo suficiente",
        "artifact": "test_ia_gerado.py / test_flask_client.py",
    },
    "test_transferencia_valor_nao_positivo_retorna_422": {
        "id": "TC-S3-001",
        "requirement": "REQ-TRF-002 - Recusar valor zero ou negativo",
        "artifact": "test_hypothesis.py",
    },
    "test_transferencia_conta_origem_inexistente": {
        "id": "TC-S4-001",
        "requirement": "REQ-TRF-003 - Recusar conta inexistente",
        "artifact": "test_flask_client.py",
    },
    "test_aceitar_transferencia_de_pequeno_valor_positivo": {
        "id": "TC-S5-001",
        "requirement": "REQ-TRF-004 - Aceitar qualquer valor positivo com saldo suficiente",
        "artifact": "features/transferencia.feature",
    },
    "test_recusar_transferencia_sem_conta_de_destino": {
        "id": "TC-S5-002",
        "requirement": "REQ-TRF-005 - Recusar transferencia com campo obrigatorio ausente",
        "artifact": "features/transferencia.feature",
    },
}


def status_for(testcase):
    if testcase.find("failure") is not None:
        return "FAILED"
    if testcase.find("error") is not None:
        return "ERROR"
    if testcase.find("skipped") is not None:
        return "SKIPPED"
    return "PASSED"


def load_results(path):
    if not path.exists():
        raise FileNotFoundError(f"Arquivo JUnit nao encontrado: {path}")

    tree = ET.parse(path)
    results = {}
    for testcase in tree.iter("testcase"):
        name = testcase.attrib.get("name", "")
        results[name] = {
            "status": status_for(testcase),
            "time": testcase.attrib.get("time", "0"),
        }
    return results


def main():
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else REPORT
    results = load_results(report_path)

    print("# Matriz de rastreabilidade - Sprint 8")
    print()
    print("| ID | Requisito | Caso de teste | Artefato | Evidencia |")
    print("|---|---|---|---|---|")

    for test_name, item in TRACEABILITY.items():
        result = results.get(test_name)
        if result is None:
            evidence = "NAO EXECUTADO no report.xml"
        else:
            evidence = f"{result['status']} em {result['time']}s"
        print(
            f"| {item['id']} | {item['requirement']} | {test_name} | "
            f"{item['artifact']} | {evidence} |"
        )


if __name__ == "__main__":
    main()
