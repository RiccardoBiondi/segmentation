#!/usr/bin/env pwsh

$input_dir = $args[0]
$centroids = $args[1]
$label1_dir = $args[2]
$label2_dir = $args[3]



If ( $null -eq $input_dir )
{
  Write-Error -Message "Error! Input directory not set" -Category NotSpecified
  exit 1
}
ElseIf (-not (Test-Path -Path $input_dir -PathType Container))
{
  Write-Error -Message "Error! Input directory not found" -Category ObjectNotFound
  exit 1
}


If ( $null -eq $centroids)
{
  Write-Error -Message "Error! No centroids file provided"-Category NotSpecified
  exit 1
}
ElseIf ( -not (Test-Path $centroids) )
{
  Write-Error -Message "Error! Centroids file not found" -Category ObjectNotFound
  exit 1
}


If ( $null -eq $label1_dir)
{
  Write-Error -Message "Error! Output directory for label 1 not set"-Category NotSpecified
  exit 1
}
ElseIf ( -not (Test-Path -Path $label1_dir -PathType Container) )
{
  Write-Error -Message "Error! Output directory for label1 not found" -Category ObjectNotFound
  exit 1
}


If ( $null -eq $label2_dir)
{
  Write-Error -Message "Error! Output directory for label 2 not set"-Category NotSpecified
  exit 1
}
ElseIf ( -not (Test-Path -Path $label2_dir -PathType Container) )
{
  Write-Error -Message "Error! Output directory for label 2 not found" -Category ObjectNotFound
  exit 1
}





$files = get-ChildItem -Path $input_dir*
Write-Output "Found "$files.Length" files to process"


For ($i = 0; $i -lt $files.Length; $i++)
{
  Write-Output  "* Processing " $files[$i]
  $BaseName = Get-Item $files[$i] | Select-Object -ExpandProperty BaseName
  $BaseName = $BaseName -replace "\..+"
  $label1_name = $label1_dir + $BaseName
  $label2_name = $label2_dir + $BaseName



  python -m CTLungSeg.labeling --input $files[$i] --centroids $centroids --label1 $label1_name --label2 $label2_name

  If ( $? )
  {
    Write-Output  '[done]'
  }
  Else
  {
    Write-Output '[failed]'
    exit 1
  }
}
